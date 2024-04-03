def calculate():
    try:
        num = complex(input("Enter a number: "))
        choice = input("Do you want to calculate factorial or square? (f/s): ")
        
        if choice.lower() == 'f':
            if num.imag != 0:
                print("Error: Factorial is not defined for complex numbers.")
                calculate()
            elif num.real < 0:
                print("Error: Factorial is not defined for negative numbers.")
                calculate()
            elif num.real % 1 != 0:
                print("Error: Factorial is only defined for integers.")
                calculate()
            else:
                factorial = 1
                for i in range(1, int(num.real) + 1):
                    factorial *= i
                print(f"The factorial of {num} is {factorial}.")
        
        elif choice.lower() == 's':
            square = num ** 2
            if square.imag == 0:
                print(f"The square of {num} is {square.real}.")
            else:
                print(f"The square of {num} is {square}.")
        
        else:
            print("Invalid choice. Please enter 'f' for factorial or 's' for square.")
            calculate()
    
    except ValueError:
        print("Invalid input. Please enter a number.")
        calculate()

calculate()