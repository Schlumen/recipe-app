recipes_list, ingredients_list = [], []

def take_recipe():
    name = str(input("Enter recipe name: "))
    cooking_time = int(input("Enter cooking time in minutes: "))
    ingredients = []

    while True:
        ingredient = str(input("Enter ingredient or hit enter if done: "))
        if ingredient != "":
            ingredients.append(ingredient)
        else:
            break            
    
    print("\n")

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

n = int(input("\nHow many recipes would you like to enter? "))
print("\nOK, we will collect the details now!\n")

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

print("You have entered the following recipes:")
print("---------------------------------------\n")

for recipe in recipes_list:
    cooking_time = recipe["cooking_time"]
    num_of_ingredients = len(recipe["ingredients"])
    difficulty = ""

    if cooking_time < 10 and num_of_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_of_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_of_ingredients < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and num_of_ingredients >= 4:
        difficulty = "Hard"

    print("Recipe:", recipe["name"])
    print("Cooking time (min):", cooking_time)
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty level:", difficulty)
    print("\n")
    
print("Ingredients available across all recipes")
print("----------------------------------------\n")

ingredients_list.sort()

for ingredient in ingredients_list:
    print(ingredient)