-- Read all recipes
SELECT name 
FROM Recipes;

-- Select recipe names based on the ingredient (e.g., egg)
SELECT RE.name
FROM RecipeIngredients 
JOIN Recipes RE ON RE.id = recipe_id 
WHERE ingredient_id IN (
    SELECT id 
    FROM Ingredients 
    WHERE name LIKE '%egg%'
);

-- Insert a new recipe
INSERT INTO Recipes (name, description, image, cook_time, prep_time, servings) 
VALUES ('Scrambled Eggs', 'A simple scrambled eggs recipe.', 'scrambled_eggs.jpg', '10 minutes', '5 minutes', 2);

-- Insert a new ingredient
INSERT INTO Ingredients (name) 
VALUES ('Egg');

-- Link a recipe with ingredients in RecipeIngredients table
INSERT INTO RecipeIngredients (recipe_id, ingredient_id, amount, unit, notes) 
VALUES (1, 1, '2', 'pieces', 'Use fresh eggs.');

-- Update a recipe's description
UPDATE Recipes 
SET description = 'A quick and easy scrambled eggs recipe.' 
WHERE id = 1;

-- Delete an ingredient by name
DELETE FROM Ingredients 
WHERE name = 'Egg' 
AND id NOT IN (SELECT ingredient_id FROM RecipeIngredients);

-- Read all ingredients for a specific recipe
SELECT I.name, RI.amount, RI.unit, RI.notes
FROM RecipeIngredients RI
JOIN Ingredients I ON I.id = RI.ingredient_id
WHERE RI.recipe_id = 1;

-- Count the number of recipes that use a specific ingredient
SELECT COUNT(DISTINCT RI.recipe_id) AS recipe_count
FROM RecipeIngredients RI
JOIN Ingredients I ON I.id = RI.ingredient_id
WHERE I.name LIKE '%egg%';