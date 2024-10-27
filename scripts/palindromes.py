from itertools import permutations

def find_palindromes(text):
    """
    Finds all unique palindromes that can be formed by rearranging the characters in the text.
    """
    palindromes = set()
    for length in range(2, len(text) + 1):  # Palindromes must have at least 2 characters
        for perm in permutations(text, length):
            word = "".join(perm)
            if word == word[::-1]:
                palindromes.add(word)
    return list(palindromes)

# Get input from the user
input_string = input("Enter a string: ")

# Find and print the palindromes
result = find_palindromes(input_string)
print("Possible palindromes:", result)