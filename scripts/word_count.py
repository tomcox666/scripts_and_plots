# It counts the number of words, lines, and characters in the provided text.

import os

def count_words(text):
    """
    Counts the number of words in a text.

    Args:
    - text (str): The input text.

    Returns:
    - int: The number of words in the text.
    """
    words = text.split()
    return len(words)

def count_lines(text):
    """
    Counts the number of lines in a text.

    Args:
    - text (str): The input text.

    Returns:
    - int: The number of lines in the text.
    """
    lines = text.split('\n')
    return len(lines)

def count_characters(text):
    """
    Counts the number of characters in a text.

    Args:
    - text (str): The input text.

    Returns:
    - int: The number of characters in the text.
    """
    return len(text)

if __name__ == "__main__":
    # Prompt the user to choose between file input and text input
    input_type = input("Do you want to input a file path (F) or a text string (T) for analysis? ").upper()

    if input_type == 'F':
        # Prompt user for the file path
        file_path = input("Enter the path to the text file: ")

        # Check if the file exists
        if not os.path.exists(file_path):
            print("File not found.")
            exit()

        # Read text from the file
        with open(file_path, 'r') as file:
            text = file.read()
    elif input_type == 'T':
        # Input text directly
        text = input("Enter the text for analysis: ")
    else:
        print("Invalid input type. Please choose either 'F' for file path or 'T' for text string.")
        exit()

    word_count = count_words(text)
    line_count = count_lines(text)
    char_count = count_characters(text)

    print("Word count:", word_count)
    print("Line count:", line_count)
    print("Character count:", char_count)