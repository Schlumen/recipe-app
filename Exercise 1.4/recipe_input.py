import pickle

def calc_diffficulty(cooking_time, ingredients):
    num_of_ingredients = len(ingredients)

    if cooking_time < 10 and num_of_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_of_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_of_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_of_ingredients >= 4:
        return "Hard"

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

    return {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": calc_diffficulty(cooking_time, ingredients)
    }

filename = input("Enter the filename where you have stored your binary file: ")

try:
    file = open(filename, "rb")
    data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
except:
    print("An unexpected error occured.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    file.close()
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

n = int(input("How many recipes would you like to enter? "))
print("OK, we will collect the details now!")

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)

data["recipes_list"] = recipes_list
data["all_ingredients"] = all_ingredients

with open(filename, "wb") as file:
    pickle.dump(data, file)
