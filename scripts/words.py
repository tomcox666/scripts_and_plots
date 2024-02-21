# It counts the number of words, lines, and characters in the provided text.

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
    # Sample text for text processing
    sample_text = """
    Python is a versatile programming language.
    It is used for web development, data science, artificial intelligence, and more.
    Learning Python is fun and rewarding.
    """

    word_count = count_words(sample_text)
    line_count = count_lines(sample_text)
    char_count = count_characters(sample_text)

    print("Word count:", word_count)
    print("Line count:", line_count)
    print("Character count:", char_count)