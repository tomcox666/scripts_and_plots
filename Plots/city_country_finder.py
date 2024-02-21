import os
from collections import Counter
from colorama import Fore
import re

def strip_text_in_parentheses(text):
    """Strip text within parentheses."""
    pattern = r'\([^)]*\)'
    return re.sub(pattern, '', text).strip()

def search_capital_cities(file_name, letters):
    """Search for matching cities or countries."""
    # Read data from the file
    with open(file_name, 'r') as file:
        # Skip the header line
        next(file)
        data = file.readlines()

    # Prepare the input letters for comparison
    letters_count = Counter(letters.lower())

    # Search for matching cities or countries
    matches = []
    for line in data:
        match = False
        # Strip whitespace and split line into components
        components = line.strip().split('\t')
        if len(components) >= 2:
            city, country = components[:2]
            city = strip_text_in_parentheses(city)
            # Convert city and country names to lowercase
            city_lower = city.lower()
            country_lower = country.lower()
            # Count occurrences of each letter in city and country names
            city_letter_count = Counter(city_lower)
            country_letter_count = Counter(country_lower)
            # Check if the input letters can form the city or country name
            if all(city_letter_count[letter] >= count for letter, count in letters_count.items()):
                match_type = "City"
                match = True
            if all(country_letter_count[letter] >= count for letter, count in letters_count.items()):
                if match:
                    match_type = "City and Country"
                else:
                    match_type = "Country"
                    match = True
            if match:        
                matches.append((city, country, match_type))

    return matches

if __name__ == "__main__":
    file_name = os.path.expanduser("../plot_data/capital_cities.csv")
    
    while True:
        letters = input(f"{Fore.WHITE}Enter letters to search for (type 'exit' to quit): ")
        
        if letters.lower() == "exit":
            confirm = input("Are you sure you want to exit? (y/n): ")
            if confirm.lower() == "yes" or "y":
                break
            else:
                continue

        results = search_capital_cities(file_name, letters)

        if results:
            print(f" {Fore.GREEN}Input - {letters}")
            print(f"{Fore.WHITE}Matches:")
            for city, country, match_type in results:
                # Highlight input letters in city and country names
                # Highlight input letters in city and country names
                # Highlight input letters in city and country names
                if match_type == "City":
                    print(f" {Fore.BLUE}{city} - {country}")
                elif match_type == "Country":
                    print(f"{Fore.RED}{country}")
                elif match_type == "City and Country":
                    print(f" {Fore.MAGENTA}{city} - {country} (Match in city and country)")
        else:
            print("No matches found.")
