DROP TABLE IF EXISTS Recipes;
CREATE TABLE Recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL, 
    image TEXT NOT NULL, 
    cook_time TEXT NOT NULL, 
    prep_time TEXT NOT NULL, 
    servings INTEGER NOT NULL
);

DROP TABLE IF EXISTS Instructions;
CREATE TABLE Instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id)
);

CREATE INDEX idx_instructions_recipe_id ON Instructions(recipe_id);

DROP TABLE IF EXISTS Images;

DROP TABLE IF EXISTS Ingredients;
CREATE TABLE Ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS RecipeIngredients;
CREATE TABLE RecipeIngredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount TEXT NOT NULL,
    unit TEXT NOT NULL,
    notes TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
);

CREATE INDEX idx_recipe_ingredients_recipe_id ON RecipeIngredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient_id ON RecipeIngredients(ingredient_id);