from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_required
import bcrypt
import logging
import pandas as pd
from flask_toastr import Toastr
from authentic import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from recipe_modal import db, Recipe , User
from functools import wraps
import json
from flask import Flask, abort, jsonify
from sqlalchemy import create_engine, func
from flask_mysqldb import MySQL
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db.init_app(app)  

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'recipe_bite'

mysql = MySQL(app)
toastr = Toastr(app)

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/recipe_bite")
connection = engine.connect()
logging.basicConfig(filename='help.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@login_manager.user_loader
def load_user(user_id):
    session = db.session  
    return session.get(User, user_id)  

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('Page not found: %s', request.url)
    return render_template('404.html', error_message="Page not found"), 404

@app.errorhandler(Exception)
def server_error(error):
    app.logger.exception('Server error occurred')
    return render_template('500.html', error_message="Internal Server Error"), 500

# Routes
@app.route('/')
def index():
    tracking_id = 'GG'
    if 'username' in session:            # If User is already logged in, redirect to home
        return redirect(url_for('home'))
    return render_template('login.html',tracking_id=tracking_id)


# Home page 
@app.route('/home')
@login_required
def home():
    top_images = [
        url_for('static', filename='images/top/top2.png'),
        url_for('static', filename='images/top/top3.png'),
        url_for('static', filename='images/top/top5.png'),
        url_for('static', filename='images/top/top6.png'),
        url_for('static', filename='images/top/top7.png'),
    ]
    top_images_json = json.dumps(top_images) 
    return render_template('home.html', top_images_json=top_images_json)


# Signup Page - To create new account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:       # If User is already logged in, redirect to home
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('signup'))
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)  
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


# Login Page - To gain access 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:        # If User is already logged in, redirect to home
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_email = '@' in username
        if is_email:
            user = User.query.filter_by(email=username).first()
        else:
            user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')
    return render_template('login.html')


#Logout - Terminate Session
@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


# Profile Page
@app.route('/profile')
@login_required
def profile():
    try:
        username = session.get('username')       # Get the username from the session
        if not username:
            abort(401)                           # Unauthorized if no user is logged in
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        data = cur.fetchall()
        cur.close()
        return render_template('profile.html', data=data)
    except Exception as e:
        print("An error occurred:", e)
        abort(500)


# Search page
@app.route('/search.html')
@login_required
def search_html():
    query = request.args.get('query', '') 
    min_rating = request.args.get('min_rating')
    ingredients = request.args.get('ingredients', '')
    category = request.args.get('category', '')
    if query:
        results = search_recipe(query, min_rating, ingredients,category)
    else:
        results = []
    return render_template('search.html', results=results, query=query)

def search_recipe(recipe_name, min_rating=None, ingredients=None, category=None):
    try:
        recipes_query = Recipe.query.filter(Recipe.name.ilike(f'%{recipe_name}%'))
        if min_rating is not None:                  
            recipes_query = recipes_query.filter(Recipe.rating >= min_rating)
            selected_ingredients = ingredients.split(',')              
            for ingredient in selected_ingredients:
                recipes_query = recipes_query.filter(func.lower(Recipe.ingredients).contains(func.lower(ingredient)))
        if category:
            selected_category = category.split(',')
            recipes_query = recipes_query.filter(Recipe.category.in_(selected_category))
        recipes = recipes_query.all()
        return [recipe.__dict__ for recipe in recipes]
    except Exception as e:
        print(e)
        return []


# Detail page
@app.route('/detail_by_name/<string:recipe_name>')
@login_required
def detail_by_name(recipe_name):
    try:
        recipe = Recipe.query.filter_by(name=recipe_name).first()
        if recipe:
            in_profile = False                      # Check if the recipe is in the user's profile
            if 'username' in session:
                username = session['username']
                user = User.query.filter_by(username=username).first()
            if user:
                preferences = user.preferences1
                if preferences:
                    if recipe_name in preferences.split(', '):
                        in_profile = True
            recipe_details = {
                'id': recipe.id,
                'name': recipe.name,
                'url' : recipe.url,
                'image_url' : recipe.image_url,
                'category': recipe.category,
                'summary': recipe.summary,
                'rating': recipe.rating,
                'rating_count': recipe.rating_count,
                'ingredients': recipe.ingredients,
                'directions': recipe.directions,
                'total': recipe.total,
                'servings': recipe.servings,
                'calories': recipe.calories,
                'carbohydrates_g': recipe.carbohydrates_g,
                'sugars_g': recipe.sugars_g,
                'fat_g': recipe.fat_g,
                'saturated_fat_g': recipe.saturated_fat_g,
                'cholesterol_mg': recipe.cholesterol_mg,
                'protein_g': recipe.protein_g,
                'dietary_fiber_g': recipe.dietary_fiber_g,
                'sodium_mg': recipe.sodium_mg,
                'in_profile': in_profile 
            }
            return render_template('recipe_details.html', recipe=recipe_details)
        else:
            return f"Recipe '{recipe_name}' not found."
    except Exception as e:
        print("An error occurred:", e)
        abort(500) 


#Update Profile - Upadate recipe to the user's profile
@app.route('/update-profile', methods=['POST'])
def update_profile():
    try:                    # Get the recipe name and action from the AJAX request
        recipe_name = request.form['recipe_name']
        action = request.form['action']
        username = session.get('username')              # Get the username from the session
        user = User.query.filter_by(username=username).first()
        if user:
            existing_preferences = user.preferences1.split(', ') if user.preferences1 else []
            if action == 'add':
                if recipe_name not in existing_preferences:
                    existing_preferences.append(recipe_name)
            elif action == 'remove':
                if recipe_name in existing_preferences:
                    existing_preferences.remove(recipe_name)
            user.preferences1 = ', '.join(existing_preferences)
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': 'Failed to update profile'}), 500


#Add Recipe
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO custom (name, ingredients, instructions) VALUES (%s, %s, %s)", (name, ingredients, instructions))
        mysql.connection.commit()
        cur.close()
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('profile'))
    return 'Invalid request'


# Handle the rating submission
def calculate_new_rating(current_rating, rating_count, new_rating):
    new_rating_count = rating_count + 1
    new_rating = max(0, min(new_rating, 5))    # Limit the new rating to be between 0 and 5
    new_rating_total = (current_rating * rating_count) + new_rating
    new_rating_average = new_rating_total / new_rating_count
    return new_rating_average, new_rating_count

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json
    current_rating = float(data['current_rating'])
    rating_count = int(data['rating_count'])
    new_rating = int(data['new_rating'])
    recipe_id = int(data['recipe_id'])
    new_rating_average, new_rating_count = calculate_new_rating(current_rating, rating_count, new_rating)
    new_rating_average = round(new_rating_average, 2)
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE recipe
            SET rating = %s, rating_count = %s
            WHERE id = %s
        """, (new_rating_average, new_rating_count, recipe_id))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"An error occurred while updating the database: {e}")
        return jsonify({'error': 'An error occurred while updating the database.'}), 500
    # Return JSON response with new rating average and count
    return jsonify({'new_rating_average': new_rating_average, 'new_rating_count': new_rating_count})


# recommendation page
@app.route('/recommended')
@login_required
def recommended():
    try:
        username = session.get('username')
        # print(username)
        if not username:
            abort(401)  # Unauthorized if no user is logged in
        cur = mysql.connection.cursor()
        cur.execute("SELECT preferences1 FROM user WHERE username = %s", (username,))
        preferences = cur.fetchone()
        if not preferences or not preferences[0]:  # If no preferences or preferences are empty
            return render_template('recommended.html', preferences=None, recipe_names=None)
        preferences_string = preferences[0]
        preference_ids = preferences_string.split(',')
        recipe_names = []
        for pref_id in preference_ids:
            query = f"SELECT ingredients FROM recipe WHERE name = '{pref_id.strip()}'"
            with mysql.connection.cursor() as cursor:
                cursor.execute(query)
                recipe_name = cursor.fetchone()[0]  # Assuming name is a single field
                recipe_names.append(recipe_name)
        recipe_query = "SELECT name, ingredients ,image_url,category  FROM recipe"
        recipes_df = pd.read_sql(recipe_query,mysql.connection)

        def calculate_ingredient_similarity(user_preferences, recipes):
            vectorizer = TfidfVectorizer(stop_words='english')
            recipe_tfidf = vectorizer.fit_transform(recipes)
            user_pref_tfidf = vectorizer.transform(user_preferences)
            similarity_scores = cosine_similarity(user_pref_tfidf, recipe_tfidf)
            return similarity_scores

        def recommend_recipes_by_ingredients(user_preferences):
            user_preferences = [user_preferences]
            similarity_scores = calculate_ingredient_similarity(user_preferences, recipes_df['ingredients']).flatten()
            top_recipe_indices = similarity_scores.argsort()[::-1]
            top_similarities = similarity_scores[top_recipe_indices]
            top_recipes = recipes_df.iloc[top_recipe_indices][:10]  # Select top 10 recommended recipes
            return top_recipes, top_similarities
        recipe_names = ' '.join(recipe_names)
        recommended_recipes_ingredients, similarity_scores = recommend_recipes_by_ingredients(recipe_names)
        recommended_recipe_names = recommended_recipes_ingredients['name'].tolist()
        similarity_scores_list = similarity_scores.tolist()
        zipped_recommendations = zip(recommended_recipe_names, similarity_scores_list)
        recipe_bar = []
        for (recipe_name, similarity_score) in zip(recommended_recipe_names, similarity_scores_list):
            recipe_data = recipes_df[recipes_df['name'] == recipe_name].iloc[0]
            in_profile = recipe_name in preferences_string            # Check if the recommended recipe is in the user's profile
            recipe_bar.append({
                'name': recipe_name,
                'category': recipe_data['category'],
                'image_url': recipe_data['image_url'],
                'similarity_score': similarity_score,
                'in_profile': in_profile
            })
        return render_template('recommended.html',recipe_bar=recipe_bar, preferences=preferences[0], recommendations=zipped_recommendations)
    except Exception as e:
        print("An error occurred:", e)
        abort(500)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')         # app.run(debug=True)
