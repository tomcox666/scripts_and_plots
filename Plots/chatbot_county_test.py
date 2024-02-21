import pandas as pd
import re

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../plot_data/allCountries.csv', sep='\t')

# Get the user input
search_term = input("Enter a search term: ")

# Define a function to highlight the matched text
def highlight_match(text):
    return '\033[91m' + text + '\033[0m'

# Filter the DataFrame to rows that contain the search term in City/Town or Country/Territory
results = df[(df['name'].str.contains(search_term, case=False)) | (df['country_code'].str.contains(search_term, case=False))]

# Loop through the filtered rows and highlight the matched text
for index, row in results.iterrows():
    city_match = re.search(search_term, row['name'])
    country_match = re.search(search_term, row['country_code'])
    
    if city_match:
        row['name'] = highlight_match(city_match.group())
    elif country_match:
        row['country_code'] = highlight_match(country_match.group())

# Print the filtered and highlighted rows
print(results.to_string(index=False))