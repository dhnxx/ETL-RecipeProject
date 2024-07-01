import requests
from bs4 import BeautifulSoup
import csv
import os
import re

BASE_URL = "https://panlasangpinoy.com/categories/recipes/"
BUZZ = ["how to cook", "how to make", "recipe", "easy to cook", "easy", "panlasang pinoy, crispy, killer"]
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
    execute()
    
def execute():
    scraped_dir = 'scraped/raw_links'
    os.makedirs(scraped_dir, exist_ok=True)

    for key, value in CATEGORIES.items():
        result = scrape_recipes(value)
        save_to_csv(scraped_dir, key, result)
        print(f"{key.title()} recipes complete.")

    print("Scraping complete.")

def scrape_recipes(url_suffix):

    url = f"{BASE_URL}/{url_suffix}/page/"

    try:
        # Initial Fetch for getting the last pagination number
        response = requests.get(url + '1')
        soup = BeautifulSoup(response.content, 'html.parser')
        pagination_last = int(soup.find('li', class_='pagination-next').find_previous_sibling('li').text.strip()[-1])
    except (requests.exceptions.RequestException, AttributeError) as e:
        print(f"Error fetching data")
        return []

    recipes = []

    for page_num in range(1, pagination_last + 1):
        page_url = f"{url}{page_num}"
        try:
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            recipe_titles = soup.find_all('a', class_='entry-title-link')

            for recipe in recipe_titles:
                title = recipe.text
                for word in BUZZ:
                    title = re.sub(word, '', title, flags=re.IGNORECASE).strip()
                title = re.sub(r'[^\w\s\'\,]+', '', title)
                title = re.sub(r'\s+', ' ', title).strip()

                recipes.append({'title': title, 'link': recipe['href']})
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page")

    return recipes

def save_to_csv(scraped_dir, category, recipes):
    filename = f"{scraped_dir}/{category}_recipes.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link'])
        writer.writeheader()
        writer.writerows(recipes)

if __name__ == '__main__':
    main()
