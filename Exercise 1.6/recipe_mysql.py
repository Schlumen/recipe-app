import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute("CREATE TABLE IF NOT EXISTS Recipes (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), ingredients VARCHAR(255), cooking_time INT, difficulty VARCHAR(20))")

def main_menu(conn, cursor):
    choice = ""
    while (choice != "quit"):
        print("\nMAIN MENU\n===========================================\nPick a choice:")
        print("\t1. Create a new recipe")
        print("\t2. Search for a recipe by ingredient")
        print("\t3. Update an existing recipe")
        print("\t4. Delete a recipe")
        print("\tType 'quit' to exit the program")
        choice = input("Your choice: ")

        if choice == "1": create_recipe(conn, cursor)
        elif choice == "2": search_recipe(conn, cursor)
        elif choice == "3": update_recipe(conn, cursor)
        elif choice == "4": delete_recipe(conn, cursor)

def create_recipe(conn, cursor):
    name = str(input("Enter recipe name: "))
    cooking_time = int(input("Enter cooking time in minutes: "))
    ingredients = []

    while True:
        ingredient = str(input("Enter ingredient or hit enter if done: "))
        if ingredient != "":
            ingredients.append(ingredient)
        else:
            break

    difficulty = calc_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)

    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, ingredients_str, cooking_time , difficulty)
    cursor.execute(sql, val)
    conn.commit()

def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []

    for row in results:
        ingredient_list = row[0].split(", ")
        for ingredient in ingredient_list:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)

    for count, ingredient in enumerate(all_ingredients):
        print(count, ingredient)

    try:
        search_ingredient = all_ingredients[int(input("Enter the index number of the ingredient that you want to search for: "))]
    except:
        print("Warning: Input is incorrect!")
    else:
        cursor.execute("SELECT name, cooking_time, ingredients, difficulty FROM Recipes WHERE ingredients LIKE %s", ("%" + search_ingredient + "%",))
        results = cursor.fetchall()

        for recipe in results:
            display_recipe(recipe)

def update_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()

    for recipe in results:
        print(recipe[0], recipe[1])

    id = int(input("\nPlease enter the id number of the recipe that you want to update: "))
    cursor.execute("SELECT name, cooking_time, ingredients, difficulty FROM Recipes WHERE id = " + str(id))
    results = cursor.fetchall()

    print("\nYou selected the following recipe:")
    display_recipe(results[0])

    difficulty = results[0][3]
    column = input("\nWhich property of the recipe would you like to update?\nN - Name\nC - Cooking time\nI - Ingredients\nType the corresponding letter: ")

    if column.upper() == "N":
        name = input("Please input new name: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (name, id))
    elif column.upper() == "C":
        cooking_time = int(input("Please input new cooking time in minutes: "))
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (cooking_time, id))
        difficulty = calc_difficulty(cooking_time, results[0][2])
    elif column.upper() == "I":
        ingredients = []
        print("Please enter the new list of ingredients - all other ingredients will be deleted")

        while True:
            ingredient = str(input("Enter ingredient or hit enter if done: "))
            if ingredient != "":
                ingredients.append(ingredient)
            else:
                break

        ingredients_str = ", ".join(ingredients)
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (ingredients_str, id))
        difficulty = calc_difficulty(results[0][1], ingredients)
    else: return

    if difficulty != results[0][3]:
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, id))

    conn.commit()

def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()

    for recipe in results:
        print(recipe[0], recipe[1])

    id = int(input("\nPlease enter the id number of the recipe that you want to delete: "))
    cursor.execute("DELETE FROM Recipes WHERE id = " + str(id))
    conn.commit()

def display_recipe(recipe):
    print("\n" + recipe[0])
    print("Cooking time (min):", recipe[1])
    print("Ingredients:")
    for ingredient in recipe[2].split(", "):
        print("  - " + ingredient)
    print("Difficulty level:", recipe[3])

def calc_difficulty(cooking_time, ingredients):
    num_of_ingredients = len(ingredients)

    if cooking_time < 10 and num_of_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_of_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_of_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_of_ingredients >= 4:
        return "Hard"

main_menu(conn, cursor)
conn.commit()
conn.close()