first_value = float(input("Please input first number: "))
second_value = float(input("Please input second number: "))
operator = input("Please input operator: ")

if operator == "+":
    print("Result:", first_value + second_value)

elif operator == "-":
    print("Result:", first_value - second_value)

else:
    print("Invalid operator")