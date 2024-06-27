#Update CSV file with output image_url
import pandas as pd
from recipe_scrapers import scrape_me

input_csv_file = 'cleaner_recipe.csv'
output_csv_file = 'result1.csv'  # id,name,url,image_url

df_input = pd.read_csv(input_csv_file)

def process_url(id, name, url):
    scraper = scrape_me(url)
    image_url = scraper.image()
    print(f"{id} : Processed {name}")
    result = {'id': id, 'name': name, 'url': url, 'image_url': image_url}
    return result

def main():
    results = []
    for index, row in df_input.iterrows():
        if 1 <= index <= 10:        # Range
            id = row['id']
            name = row['name']
            url = row['url']
            result = process_url(id, name, url)
            results.append(result)

    df_output = pd.DataFrame(results)
    df_output.to_csv(output_csv_file, index=False)

    print("Output CSV file created successfully.")

if __name__ == "__main__":
    main()
