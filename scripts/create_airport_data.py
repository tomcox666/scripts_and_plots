import pandas as pd
import random


# Define a dictionary for airport and airline information
airports = {
    'US': {
        'OREGON': ['PDX - Portland', 'EUG - Eugene'],
        'CALIFORNIA': ['SFO - San Francisco', 'LAX - Los Angeles'],
        'WASHINGTON': ['SEA - Seattle', 'GEG - Spokane']
    },
    'EU': {
        'FRANCE': ['CDG - Paris', 'ORY - Paris'],
        'GERMANY': ['FRA - Frankfurt', 'MUC - Munich'],
        'UK': ['LHR - London', 'LGW - London']
    }
}


airlines = {
    'US': ['ALASKA AIRLINES', 'DELTA', 'UNITED AIRLINES', 'AMERICAN AIRLINES', 'SOUTHWEST AIRLINES', 'JETBLUE', 'SPIRIT AIRLINES'],
    'EU': ['AIR FRANCE', 'EASYJET', 'LUFTHANSA', 'BRITISH AIRWAYS']
}


# Function to generate random data
def generate_random_data(location, num_rows):
    data = []
    for _ in range(num_rows):
        or_state = random.choice(list(airports[location].keys()))
        airport = random.choice(airports[location][or_state])
        airline = random.choice(airlines[location])
        num_flights = random.randint(50, 150)
        avg_delay = random.randint(-10, 20)
        data.append([location, or_state, airport, airline, num_flights, avg_delay])
    return data


# Generate data for US and EU
us_data = generate_random_data('US', 1000)
eu_data = generate_random_data('EU', 1000)


# Combine data and create DataFrame
data = us_data + eu_data
df = pd.DataFrame(data, columns=['LOCATION', 'OR_STATE', 'AIRPORT', 'AIRLINE', 'NUM_OF_FLIGHTS_BY_AIRLINE_AIRPORT', 'AVG_DELAY_BY_AIRLINE'])


# Save to CSV file
df.to_csv('../plot_data/air_traffic_data.csv', index=False)