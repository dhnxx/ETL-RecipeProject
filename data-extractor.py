import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import json

CATEGORIES = {
    "chicken": 'chicken-recipes',
    "pork": 'pork-recipes',
    "beef": 'beef-recipes',
    "vegetable": 'vegetable-recipes',
    "dessert": 'dessert-and-pastry-recipes',
    "pasta": 'pasta-recipes',
    "fish": 'fish-recipes-recipes',
    "noodles": 'noodle-recipes',
    "rice": 'rice-recipes',
    "egg": 'eggs',
    "crab": 'crab-recipes',
    "squid": 'squid-recipes',
    "pulutan": 'pulutan-recipes',
    "tofu": 'tofu-recipes-recipes',
    "shrimp": 'shrimp-recipes',
}

BUZZ = ["how to cook", "how to make", "recipe", "easy to cook", "easy", "panlasang pinoy", "crispy", "killer", "version"]

def main():
    value = checker()
    if not value:
        print("Data not complete. Please run link-scraper.py first.")
        return

    print("Data complete. Proceeding to data extraction.")
    execute()

def checker():
    if not os.path.exists("scraped/raw_links"):
        return False
    
    for key, value in CATEGORIES.items():
        if not os.path.exists(f"scraped/raw_links/{key}_recipes.csv"):
            return False
        
    return True

def execute():
    scraped_dir = 'scraped/raw_data'
    os.makedirs(scraped_dir, exist_ok=True)

    for key, value in CATEGORIES.items():
        data = extract_data(f"scraped/raw_links/{key}_recipes.csv")
        print(f"Finished extracting {key} recipes.")
        save_to_csv(key, data)
    
    print("Data extraction complete.")

def extract_data(file_path):
    links = []
    data = []

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append(row['link'])
    
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        recipe_container = soup.find('div', class_='oc-recipe-container')

        # Exclude the recipe if it does not have the necessary elements
        if not recipe_container:
            continue

        title = recipe_container.find('h2', class_='wprm-recipe-name').text if recipe_container.find('h2', class_='wprm-recipe-name') else ''

        # Remove buzzwords from title
        for word in BUZZ:
            title = re.sub(word, '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'[^\w\s\'\,]+', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        prep_time = recipe_container.find('span', class_='wprm-recipe-prep_time-minutes').text if recipe_container.find('span', class_='wprm-recipe-prep_time-minutes') else ''
        cook_time = recipe_container.find('span', class_='wprm-recipe-cook_time-minutes').text if recipe_container.find('span', class_='wprm-recipe-cook_time-minutes') else ''
        servings = recipe_container.find('span', class_='wprm-recipe-servings').text if recipe_container.find('span', class_='wprm-recipe-servings') else ''
        
        # Get the ingredients
        raw_ingredients = []

        for ingredient in soup.find_all('li', class_='wprm-recipe-ingredient'):
            raw_ingredients.append(
                {
                    'name': ingredient.find('span', class_='wprm-recipe-ingredient-name').get_text(strip=True) 
                    if ingredient.find('span', class_='wprm-recipe-ingredient-name') else '',
                    'amount': ingredient.find('span', class_='wprm-recipe-ingredient-amount').get_text(strip=True) 
                    if ingredient.find('span', class_='wprm-recipe-ingredient-amount') else '',
                    'unit': ingredient.find('span', class_='wprm-recipe-ingredient-unit').get_text(strip=True) 
                    if ingredient.find('span', class_='wprm-recipe-ingredient-unit') else '',
                    'notes': ingredient.find('span', class_='wprm-recipe-ingredient-notes').get_text(strip=True) 
                    if ingredient.find('span', class_='wprm-recipe-ingredient-notes') else '',
                }
            )

        ingredients = json.dumps(raw_ingredients)

        # Get the instructions
        raw_instructions = []

        instructions = recipe_container.find_all('div', class_='wprm-recipe-instruction-text')
        for instruction in instructions:
            raw_instructions.append(instruction.text)

        instructions = json.dumps(raw_instructions)
        
        # Get the image
        try:
            image_container = recipe_container.find('div', class_='wprm-recipe-image')
            image = image_container.find('img')
            if 'data-lazy-src' in image.attrs:
                image = image['data-lazy-src']
            else:
                image = image['src']
        except:
            image = 'NA'

        # Get the description 
        description = None

        # Get the description 
        description_container = recipe_container.find('div', class_='wprm-recipe-summary')

        if description_container:
            description_span = description_container.find('span')
            if description_span:
                description = description_span.text


        # Append the data to the list
        data.append(
            [
                title if title else 'NA',
                prep_time if prep_time else 'NA',
                cook_time if cook_time else 'NA',
                servings if servings else 'NA',
                image if image else 'NA',
                ingredients if ingredients else 'NA',
                instructions if instructions else 'NA',
                description if description else 'NA'
            ]
        )

    return data

def save_to_csv(key, data):
    headers = ["Title", "Prep Time", "Cook Time", "Servings", "Image", "Ingredients", "Instructions", "Description"]
    with open(f'scraped/raw_data/{key}_recipes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)


if __name__ == "__main__":
    main()
