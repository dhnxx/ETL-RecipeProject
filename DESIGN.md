# DESIGN.md

## Purpose
The primary purpose of this database is to store scraped data from the Panlasang Pinoy website, with the eventual goal of using the data in a backend or for a mobile app. This database aims to provide users with an efficient way to access and manipulate recipe data for cooking and meal planning.

## Scope
The scope of this database includes the following key features and functionalities:
- Storing recipes, including their ingredients, cooking instructions, and metadata such as prep and cook times, serving sizes, and images.
- Enabling efficient retrieval of recipes based on ingredient searches, making it easier for users to find what they can cook based on available ingredients.
- Supporting future enhancements to integrate with a mobile application or backend service, allowing seamless data access for end-users.

Limitations of the current design include:
- Lack of user authentication or personalized features, meaning users cannot save favorite recipes or contribute new recipes.
- No support for filtering recipes based on dietary restrictions, cuisine types, or advanced search functionalities that may enhance user experience.

## Entities
The main entities in the database are:
- **Recipes**: This table consists of attributes:
  - `id`: INTEGER (Primary Key)
  - `name`: TEXT (Recipe name)
  - `description`: TEXT (Brief description of the recipe)
  - `image`: TEXT (URL or path to an image of the recipe)
  - `cook_time`: TEXT (Time taken to cook)
  - `prep_time`: TEXT (Time taken to prepare)
  - `servings`: INTEGER (Number of servings)

- **Ingredients**: This table contains:
  - `id`: INTEGER (Primary Key)
  - `name`: TEXT (Name of the ingredient)

- **Instructions**: Attributes include:
  - `id`: INTEGER (Primary Key)
  - `step_number`: INTEGER (Step order for instructions)
  - `description`: TEXT (Description of the cooking step)
  - `recipe_id`: INTEGER (Foreign Key referencing `Recipes(id)`)

- **RecipeIngredients**: This junction table includes:
  - `id`: INTEGER (Primary Key)
  - `recipe_id`: INTEGER (Foreign Key referencing `Recipes(id)`)
  - `ingredient_id`: INTEGER (Foreign Key referencing `Ingredients(id)`)
  - `amount`: TEXT (Quantity of the ingredient)
  - `unit`: TEXT (Measurement unit for the ingredient)
  - `notes`: TEXT (Any additional notes about the ingredient)

## Relationships
The relationships between entities are primarily one-to-many:
- Each recipe can have multiple instructions and ingredients, ensuring that detailed step-by-step guidance is provided for each recipe.
- Each ingredient can be associated with multiple recipes through the `RecipeIngredients` junction table, allowing for efficient tracking of ingredient usage across various recipes.

Foreign keys maintain referential integrity, ensuring that any `recipe_id` in `Instructions` or `RecipeIngredients` corresponds to an existing entry in the `Recipes` table. This helps to prevent orphan records and maintain data consistency.

## Optimizations
To enhance query performance, indexes have been created on the `recipe_id` columns in both the `Instructions` and `RecipeIngredients` tables. These indexes facilitate quicker lookups and improve the efficiency of join operations, especially when searching for recipes based on specific ingredients or retrieving associated instructions.

## Limitations
Known limitations of this database design include:
- The absence of user-specific functionalities, such as saving favorite recipes or custom user inputs. As a result, the application may not fully cater to personalized user experiences.
- Current search functionalities are limited to ingredient names; more complex queries, such as filtering recipes by multiple criteria (e.g., preparation time, dietary restrictions), are not supported in the current design.

Future enhancements may include implementing user accounts, advanced filtering options, and possibly integrating a recommendation system based on user preferences and cooking history.

## Additional Considerations
Security measures are essential, especially in terms of data validation to prevent SQL injection and ensure data integrity. Input from the scraping process will be validated to conform to expected formats and values, minimizing the risk of corrupt data being inserted into the database.

To maintain data integrity and avoid duplicates, normalization techniques have been employed. Ingredients are checked for existence before being added to the `Ingredients` table, ensuring that common ingredients like "salt" or "egg" are stored only once, with references in the `RecipeIngredients` table.

In future iterations, enhancements such as user authentication, a mobile app interface, and expanded search capabilities will be considered to improve the overall user experience and functionality of the application.
