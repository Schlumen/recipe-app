class Recipe:
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = ""
    
    def get_name(self):
        return self.name
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def get_ingredients(self):
        return self.ingredients
    
    def get_difficulty(self):
        if self.difficulty == "":
            self.calculate_difficulty()
        return self.difficulty
    
    def set_name(self, name):
        self.name = name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = int(cooking_time)

    def add_ingredients (self, *ingredients):
        for ingredient in ingredients:
            if not ingredient in self.ingredients:
                self.ingredients.append(ingredient)

        self.update_all_ingredients()

    def calculate_difficulty(self):
        num_of_ingredients = len(self.ingredients)

        if self.cooking_time < 10 and num_of_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_of_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_of_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_of_ingredients >= 4:
            self.difficulty = "Hard"

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not ingredient in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def __str__(self):
        outputstring = "\n" + self.get_name()
        outputstring += "\nCooking time (min): " + str(self.get_cooking_time())
        outputstring += "\nIngredients: "
        for ingredient in self.get_ingredients():
            outputstring += "\n  - " + ingredient
        outputstring += "\nDifficulty: " + self.get_difficulty()

        return outputstring

    def recipe_search(data, search_term):
        print("\nRecipes containing " + search_term)
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)

# --- End of Class and start of main code --- #

tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)

print(tea)
print(coffee)
print(cake)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

Recipe.recipe_search(recipes_list, "Water")
Recipe.recipe_search(recipes_list, "Sugar")
Recipe.recipe_search(recipes_list, "Bananas")