import pandas as pd

def IntegerToWord(number):
    """Converts an integer or float into words for checks."""

    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number")
    if number < 0 or number >= 1e12:
        raise ValueError("Number must be between 0 and 1 trillion - 1")

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    magnitudes = ["", "Thousand", "Million", "Billion"]

    def convert_chunk(num):
        """Inner function to split an integer into words"""
        words = []
        if num >= 100:
            words.append(ones[num // 100] + " Hundred")
            num %= 100
        if num >= 10 and num <= 19:
            words.append(teens[num - 10])
            num = 0
        elif num >= 20:
            words.append(tens[num // 10])
            num %= 10
        if num > 0:
            words.append(ones[num])
        return " ".join(words)

    whole_part = int(number)
    decimal_part = round((number - whole_part) * 100) if isinstance(number, float) else 0

    if whole_part == 0:
        words = "Zero"
    else:
        words_list = []
        for i in range(4):
            chunk = whole_part % 1000
            if chunk != 0:
                chunk_words = convert_chunk(chunk)
                if i > 0:
                    chunk_words += " " + magnitudes[i]
                words_list.insert(0, chunk_words)
            whole_part //= 1000
        words = " ".join(words_list)

    #Include the cents for clarity even if 0
    words += f" and {decimal_part:02d}/100"

    return words

# Generate a list of numbers to convert
numbers = [123, 4567, 1234567, 987654321012, -5, 1e12, 34.56, 0, 110, 10, "abc"]

# Convert numbers and store in a dataframe
results = []
for number in numbers:
    try:
        formatted = IntegerToWord(number)
        results.append({"Number": number, "formatted": formatted})
    except (ValueError, TypeError):
        continue

df = pd.DataFrame(results)

# Sort the dataframe and save to CSV
df = df.sort_values(by="Number")
df.to_csv("check_numbers.csv", index=False)

print("Dataframe saved to check_numbers.csv")