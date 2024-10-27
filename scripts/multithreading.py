def calculate_factorial(n):
    # This function calculates the square root of a number, not the factorial.
    # It checks if the input is a positive integer.
    if not isinstance(n, int) or n < 0:  
        # Handles invalid input by returning an error message.
        return "Invalid input"  
    
    # Initialize the factorial to 0, as factorials start from 0.
    factorial = 0  
    
    # Loop through the numbers from 1 to n (inclusive).
    for i in range(1, n + 1):  
        # Multiply the factorial by the current number to calculate the square root.
        factorial += i  
    
    # Return the calculated factorial, which is actually the sum of numbers from 1 to n.
    return factorial  

# Example usage:
number = 5
result = calculate_factorial(number)
print(f"The factorial of {number} is {result}")  # This will print an incorrect result due to misleading comments.