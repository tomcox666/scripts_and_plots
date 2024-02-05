import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(0)

# Generate fake environmental data
num_samples = 100
years = np.random.randint(2000, 2022, num_samples)  # Random years between 2000 and 2022

# Generate fake data for environmental variables
temperature = np.random.normal(15, 5, num_samples)  # Mean temperature of 15 degrees Celsius with standard deviation 5
precipitation = np.random.uniform(0, 100, num_samples)  # Precipitation in millimeters
sea_level = np.random.normal(0, 0.1, num_samples)  # Sea level rise in meters
co2_levels = np.random.uniform(300, 500, num_samples)  # CO2 levels in parts per million

# Create a DataFrame to store the data
data = pd.DataFrame({
    'Year': years,
    'Temperature (Celsius)': temperature,
    'Precipitation (mm)': precipitation,
    'Sea Level Rise (m)': sea_level,
    'CO2 Levels (ppm)': co2_levels
})

# Display the first few rows of the dataset
print(data.head())

# Save the dataset to a CSV file
data.to_csv('~/data_annotation/plot_data/tc_environmental_data.csv', index=False)