# ===============================
# Simple Calculator (Internship Level)
# ===============================

def calculator():
    print("\n===== SIMPLE CALCULATOR =====")

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except:
        print("❌ Invalid input! Please enter numbers only.")
        return

    print("\nChoose operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")

    choice = input("Enter choice (1/2/3/4): ")

    if choice == '1':
        print(f"✅ Result: {num1} + {num2} = {num1 + num2}")

    elif choice == '2':
        print(f"✅ Result: {num1} - {num2} = {num1 - num2}")

    elif choice == '3':
        print(f"✅ Result: {num1} * {num2} = {num1 * num2}")

    elif choice == '4':
        if num2 != 0:
            print(f"✅ Result: {num1} / {num2} = {num1 / num2}")
        else:
            print("❌ Error: Division by zero is not allowed!")

    else:
        print("❌ Invalid choice! Please select 1-4.")


# Loop to run calculator again and again
while True:
    calculator()
    
    again = input("\nDo you want to calculate again? (yes/no): ").lower()
    if again != 'yes':
        print(" Thank you for using calculator!")
        break