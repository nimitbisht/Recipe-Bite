import pandas as pd
from sqlalchemy import create_engine

csv_file = 'final_recipe.csv'
df = pd.read_csv(csv_file)

selected_columns = ['id','name','url','image_url', 'category', 'summary', 'rating', 'rating_count', 'ingredients', 'directions'
                    , 'total','servings','yield','calories','carbohydrates_g','sugars_g','fat_g','saturated_fat_g'
                    ,'cholesterol_mg','protein_g','dietary_fiber_g','sodium_mg']


df_selected = df[selected_columns]

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/recipe_bite")

table_name = 'recipe' 
df_selected.to_sql(table_name, con=engine, if_exists='replace', index=False)
print("Data Stored Successfully")
