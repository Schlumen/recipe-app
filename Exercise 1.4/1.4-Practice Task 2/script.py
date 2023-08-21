import pickle

recipe = {
    "Name": "Tea",
    "Ingredients": ["Tea leaves", "Water", "Sugar"],
    "Cooking time": "5 minutes",
    "Difficulty": "Easy"
}

with open("recipe_binary.bin", "wb") as my_file:
    pickle.dump(recipe, my_file)

with open("recipe_binary.bin", "rb") as my_file:
    read_recipe = pickle.load(my_file)

print("Recipe: " + read_recipe["Name"])
print("Ingredients:")
for ingredient in read_recipe["Ingredients"]:
    print("  " + ingredient)
print("Cooking time: " + read_recipe["Cooking time"])
print("Difficulty: " + read_recipe["Difficulty"])