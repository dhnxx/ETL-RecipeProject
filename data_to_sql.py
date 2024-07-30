import sqlite3
import csv
import json
import re

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

def main():
    run_schema_script()
    csv_to_sql()

def run_schema_script():
    connection = sqlite3.connect('scraped_recipes.db')
    cursor = connection.cursor()

    with open('schema.sql', 'r') as file:
        sql_script = file.read()

    cursor.executescript(sql_script)

    connection.commit()
    connection.close()

def normalize_ingredient_name(name):
    name = re.sub(r'[^\w\s\'\,]+', '', name)
    return name.strip().title()

def csv_to_sql():
    connection = sqlite3.connect('scraped_recipes.db')
    cursor = connection.cursor()

    for key, value in CATEGORIES.items():
        with open(f"scraped/raw_data/{key}_recipes.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    cursor.execute('''
                    INSERT INTO Recipes (name, description, image, prep_time, cook_time, servings)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (row['Title'], row['Description'], row['Image'], row['Prep Time'], row['Cook Time'], row['Servings']))

                    last_recipe_id = cursor.lastrowid
                    instructions = json.loads(row['Instructions'])
                    for idx, instruction in enumerate(instructions, start=1):
                        cursor.execute('''
                        INSERT INTO Instructions (description, step_number, recipe_id)
                        VALUES (?, ?, ?)
                        ''', (instruction, idx, last_recipe_id))

                    ingredients = json.loads(row['Ingredients'])
                    for ingredient in ingredients:
                        normalized_name = normalize_ingredient_name(ingredient['name'])
                        cursor.execute('''
                        SELECT id FROM Ingredients
                        WHERE name = ?
                        ''', (normalized_name,))
                        fetched_ingredient = cursor.fetchone()

                        if not fetched_ingredient:
                            cursor.execute('''
                            INSERT INTO Ingredients (name) VALUES (?)
                            ''', (normalized_name,))
                            ingredient_id = cursor.lastrowid
                        else:
                            ingredient_id = fetched_ingredient[0]
                           
                        cursor.execute('''
                        INSERT INTO RecipeIngredients (recipe_id, ingredient_id, amount, unit, notes)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (last_recipe_id, ingredient_id, ingredient['amount'], ingredient['unit'], ingredient.get('notes', '')))

                    connection.commit()
                except sqlite3.Error as e:
                    print(f"Error processing row {row}: {e}")

    connection.close()

if __name__ == "__main__":
    main()
