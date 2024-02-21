import pandas as pd
import folium

# Read the CSV files into DataFrames
df_european_capitals = pd.read_csv("../plot_data/DZPG_European_Capitals.csv")
df_us_20_largest_cities = pd.read_csv("../plot_data/DZPG_us_20_largest_cities.csv")
df_usa_state_capitals = pd.read_csv("../plot_data/DZPG_USA_State_Capitals.csv")

# Rename columns to match
df_european_capitals.rename(columns={'Country': 'Country/State'}, inplace=True)
df_us_20_largest_cities.rename(columns={'city': 'City', 'population': 'Population', 'latitude': 'Latitude', 'longitude': 'Longitude'}, inplace=True)
df_usa_state_capitals.rename(columns={'capital': 'City', 'state': 'Country/State', 'latitude': 'Latitude', 'longitude': 'Longitude'}, inplace=True)

# Remove 'sum' column
df_usa_state_capitals = df_usa_state_capitals.drop(columns=['sum'])
df_usa_state_capitals = df_usa_state_capitals.loc[:, ~df_usa_state_capitals.columns.str.contains('^Unnamed')]

# Update city names in US cities DataFrame and add state names to 'Country/State' column
state_names = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 
    'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 
    'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 
    'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Add 'Country/State' column to US 20 largest cities DataFrame
df_us_20_largest_cities['Country/State'] = df_us_20_largest_cities['City'].str.extract(r',\s*(\b[A-Z]{2}\b)')

# Update city names in US cities DataFrame
df_us_20_largest_cities['City'] = df_us_20_largest_cities['City'].str.replace(r',\s*\b[A-Z]{2}\b', '')

# Apply state name conversion
df_us_20_largest_cities['Country/State'] = df_us_20_largest_cities['Country/State'].map(state_names)
df_us_20_largest_cities['City'] = df_us_20_largest_cities['City'].apply(lambda x: x.split(',')[0].strip())

# Concatenate the DataFrames
combined_df = pd.concat([df_european_capitals, df_us_20_largest_cities, df_usa_state_capitals], ignore_index=True)

population_data = {
    'Montgomery': 198218,
    'Juneau': 32476,
    'Phoenix': 1680992,
    'Little Rock': 197881,
    'Sacramento': 513624,
    'Denver': 727211,
    'Hartford': 121054,
    'Dover': 38443,
    'Washington': 702455,
    'Tallahassee': 194500,
    'Atlanta': 506811,
    'Honolulu': 337256,
    'Boise': 228959,
    'Springfield': 116250,
    'Indianapolis': 876384,
    'Des Moines': 214778,
    'Topeka': 125310,
    'Frankfort': 27704,
    'Baton Rouge': 225374,
    'Augusta': 19136,
    'Annapolis': 39331,
    'Boston': 694583,
    'Lansing': 117159,
    'St. Paul': 311527,
    'Jackson': 153701,
    'Jefferson City': 43079,
    'Helena': 32550,
    'Lincoln': 287401,
    'Carson City': 55916,
    'Concord': 43364,
    'Trenton': 83426,
    'Santa Fe': 84797,
    'Albany': 97856,
    'Raleigh': 474069,
    'Bismarck': 73931,
    'Columbus': 898553,
    'Oklahoma City': 655057,
    'Salem': 173442,
    'Harrisburg': 49528,
    'Providence': 179335,
    'Columbia': 133273,
    'Pierre': 13646,
    'Nashville': 669053,
    'Austin': 978908,
    'Salt Lake City': 200567,
    'Montpelier': 7855,
    'Richmond': 230436,
    'Olympia': 53958,
    'Charleston': 51400,
    'Madison': 259680,
    'Cheyenne': 64235,
    'San Juan': 355000
}

# Add population data to the DataFrame
combined_df['Population'] = combined_df['Population'].fillna(combined_df['City'].map(population_data))

# Set display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Display the combined DataFrame
#print(combined_df)


# Create a Folium map object centered around Europe
map = folium.Map(location=[48.8566, 2.3522], zoom_start=6)

# Create a map object
map = folium.Map(location=[48.8566, 2.3522], zoom_start=6)

# Iterate through the rows of the `combined_df` DataFrame
for index, row in combined_df.iterrows():
    city = row["City"]
    latitude = row["Latitude"]
    longitude = row["Longitude"]
    population = row["Population"]

    # Create a Folium marker for each city
    marker = folium.Marker(
        location=[latitude, longitude],
        popup=f"{city}: {population:,.0f}",
        icon=folium.Icon(color="red", icon="info-sign"),
    )

    # Add the marker to the map
    marker.add_to(map)

# Save the map to an HTML file
map.save("city_population_map.html")