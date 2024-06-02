# authentic.py

import secrets


# SECRET_KEY = secrets.token_hex(16)  
SECRET_KEY = 'your_secret_key_here'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/recipe_bite' # change According To your DB
