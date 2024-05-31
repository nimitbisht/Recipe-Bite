# recipe_modal.py

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    category = db.Column(db.Text)
    summary = db.Column(db.Text)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.BigInteger)
    ingredients = db.Column(db.Text)
    directions = db.Column(db.Text)
    total = db.Column(db.Text)
    servings = db.Column(db.BigInteger)
    calories = db.Column(db.Float)
    carbohydrates_g = db.Column(db.Float)
    sugars_g = db.Column(db.Float)
    fat_g = db.Column(db.Float)
    saturated_fat_g = db.Column(db.Float)
    cholesterol_mg = db.Column(db.Float)
    protein_g = db.Column(db.Float)
    dietary_fiber_g = db.Column(db.Float)
    sodium_mg = db.Column(db.Float)

    def __repr__(self):
        return f'<Recipe {self.name}>'
    


# User model
class User(UserMixin, db.Model): 
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(20), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(60), nullable=False)  
    preferences1 = db.Column(db.String(255), nullable=True)  
    def __repr__(self):
        return f'<User {self.name}>'