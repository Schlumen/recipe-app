# Import packages and methods
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

# Store declarative base class into a variable called Base
Base = declarative_base()
# Create an engine object that connects to database
engine = create_engine("mysql://cf-python:password@localhost/task_database")
# Generate the Session class and bind it to the engine
Session = sessionmaker(bind=engine)
# Initialize the session object
session = Session()

# Definition for the Recipe model
class Recipe(Base):
    # Table name
    __tablename__ = "final_recipes"
    # Table columns
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    # Show a quick representation of the recipe
    def __repr__(self):
        return "Recipe ID: " + str(self.id) + ", Name: " + self.name + ", Difficulty: " + self.difficulty
    
    # Print a well-formatted version of the recipe
    def __str__(self):
        rstr = "\nRecipe Name: " + self.name
        rstr += "\nCooking time (min): " + str(self.cooking_time)
        rstr += "\nIngredients: "
        for ingredient in self.return_ingredients_as_list():
            rstr += "\n\t" + ingredient
        rstr += "\nDifficulty: " + self.difficulty

        return rstr
    
    # Calculate the difficulty of a recipe based on the number of ingredients and cooking time
    def calculate_difficulty(self):
        num_of_ingredients = len(self.return_ingredients_as_list())

        if self.cooking_time < 10 and num_of_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_of_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_of_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_of_ingredients >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if self.ingredients == "": return []
        return self.ingredients.split(", ")

# Create the corresponding table on the database
Base.metadata.create_all(engine)

# --- Main Menu Functions --- #

# Adding new recipe
def create_recipe():
    # Getting recipe name
    while True:
        name = str(input("Enter recipe name: "))
        if len(name) > 50:
            print("Name is too long, please enter a name with a maximum of 50 characters including spaces.")
        else: break
    # Getting recipe cooking time
    while True:
        cooking_time_input = input("Enter cooking time in minutes: ")
        if not cooking_time_input.isnumeric():
            print("This is not a number. Please enter minutes as a number.")
        else:
            cooking_time = int(cooking_time_input)
            break
    # Collecting ingredients
    ingredients_list = []
    while True:
        ingredient = str(input("Enter ingredient or hit enter if done: "))
        if ingredient != "":
            ingredients_list.append(ingredient)
        else: break
    ingredients = ", ".join(ingredients_list)
    # Creating Recipe object
    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)
    recipe_entry.calculate_difficulty()
    # Adding Recipe object to database
    session.add(recipe_entry)
    session.commit()

# Show all recipes as a list to the user
def view_all_recipes():
    all_recipes = session.query(Recipe).all()
    if len(all_recipes) < 1:
        print("There are no recipes in the database!")
        return
    for recipe in all_recipes:
        print(recipe)

# Search recipes by ingrediet
def search_by_ingredients():
    # Check if any recipes exist on database
    if session.query(Recipe).count() < 1:
        print("There are no recipes in the database!")
        return
    # Get ingredients from database
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    # Convert strings into list and remove duplicates
    for str in results:
        ingredient_list = str[0].split(", ")
        for ingredient in ingredient_list:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)
    # Print all ingredients
    for count, ingredient in enumerate(all_ingredients):
        print(count, ingredient)
    # Let user select ingredients and check if input is valid
    ingredients_input = input("Enter the index number of the ingredients that you want to search for separated by space: ")
    indices = ingredients_input.split(" ")
    search_ingredients = []
    for idx in indices:
        if not idx.isnumeric():
            print("Input is not valid!")
            return
        else: idx = int(idx)
        if idx < 0 or idx >= len(all_ingredients):
            print("Input is not valid!")
            return
        # Save desired ingredients in a list
        search_ingredients.append(all_ingredients[int(idx)])
    # Search for recipes containing the desired ingredients
    conditions = []
    for search_ingredient in search_ingredients:
        like_term = "%" + search_ingredient + "%"
        conditions.append(Recipe.ingredients.like(like_term))
    recipes = session.query(Recipe).filter(*conditions).all()
    # Print all resulting recipes
    for recipe in recipes:
        print(recipe)

# Modify recipe
def edit_recipe():
    # Check if any recipes exist on database
    if session.query(Recipe).count() < 1:
        print("There are no recipes in the database!")
        return
    # Get all recipe names and IDs from database
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    # Print recipe IDs and names
    ids = []
    for recipe in results:
        print(recipe[0], recipe[1])
        ids.append(recipe[0])
    # Get ID of recipe from user
    try:
        id = int(input("Please enter the ID of the recipe that you want to update and hit enter: "))
    except:
        print("Input is invalid! Going back to main menu.")
        return
    # Check ID
    if not id in ids:
        print("ID not found! Going back to main menu.")
        return
    # Save recipe to variable and print editable properties
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == id).one()
    print("1 - Name:", recipe_to_edit.name)
    print("2 - Ingredients:", recipe_to_edit.ingredients)
    print("3 - Cooking time", recipe_to_edit.cooking_time)
    # Let user select property to update
    try:
        num = int(input("Enter the corresponding number of the attribute that you'd like to edit: "))
    except:
        print("Input is invalid! Going back to main menu.")
        return
    if num == 1:
        # Edit name
        while True:
            name = str(input("Enter new recipe name: "))
            if len(name) > 50:
                print("Name is too long, please enter a name with a maximum of 50 characters including spaces.")
            else: break
        recipe_to_edit.name = name
    elif num == 2:
        # Edit ingredients
        ingredients_list = []
        while True:
            ingredient = str(input("Enter new ingredient or hit enter if done: "))
            if ingredient != "":
                ingredients_list.append(ingredient)
            else: break
        ingredients = ", ".join(ingredients_list)
        recipe_to_edit.ingredients = ingredients
        recipe_to_edit.calculate_difficulty()
    elif num == 3:
        # Edit cooking time
        while True:
            cooking_time_input = input("Enter new cooking time in minutes: ")
            if not cooking_time_input.isnumeric():
                print("This is not a number. Please enter minutes as a number.")
            else:
                cooking_time = int(cooking_time_input)
                break
        recipe_to_edit.cooking_time = cooking_time
        recipe_to_edit.calculate_difficulty()
    else:
        print("Number is invalid! Going back to main menu.")
        return
    # Commit changes
    session.commit()

# Delete recipe
def  delete_recipe():
    # Check if any recipes exist on database
    if session.query(Recipe).count() < 1:
        print("There are no recipes in the database!")
        return
    # Get all recipe names and IDs from database
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    # Print recipe IDs and names
    ids = []
    for recipe in results:
        print(recipe[0], recipe[1])
        ids.append(recipe[0])
    # Get ID of recipe from user
    try:
        id = int(input("Please enter the ID of the recipe that you want to delete and hit enter: "))
    except:
        print("Input is invalid! Going back to main menu.")
        return
    # Check ID
    if not id in ids:
        print("ID not found! Going back to main menu.")
        return
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == id).one()
    print(recipe_to_delete)
    answer = input("Are you sure to delete this recipe? (If yes, enter 'yes' and hit enter): ")
    if answer == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Deleted!")

### --- MAIN LOOP --- ###

choice = ""
while (choice != "quit"):
    print("\nMAIN MENU")
    print("=" * 50)
    print("Pick a choice:")
    print("\t1. Create a new recipe")
    print("\t2. View all recipes")
    print("\t3. Search for a recipe by ingredients")
    print("\t4. Update an existing recipe")
    print("\t5. Delete a recipe")
    print("\tType 'quit' to exit the program")
    choice = input("Your choice: ")

    if choice == "1": create_recipe()
    elif choice == "2": view_all_recipes()
    elif choice == "3": search_by_ingredients()
    elif choice == "4": edit_recipe()
    elif choice == "5": delete_recipe()
    elif choice != "quit": print("Invalid input!")

# End: Closing session and database
session.close()
engine.dispose()