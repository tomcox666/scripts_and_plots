import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("~/data_annotation/plot_data/EX97_stars.csv")

# 1. Calculate descriptive statistics
temp_stats = df['Temperature (K)'].describe()
lum_stats = df['Luminosity(L/Lo)'].describe()

print("Descriptive Statistics for Temperature (K):\n", temp_stats)
print("\nDescriptive Statistics for Luminosity(L/Lo):\n", lum_stats)

# 2. Create a box plot for "Temperature (K)"
plt.figure(figsize=(8, 5))  # Adjust figure size for better visibility
plt.boxplot(df['Temperature (K)'])
plt.xlabel("Temperature (K)")
plt.title("Box Plot of Temperature (K)")
plt.show()

# 3. Create a box plot for "Luminosity(L/Lo)"
plt.figure(figsize=(8, 5))
plt.boxplot(df['Luminosity(L/Lo)'])
plt.xlabel("Luminosity(L/Lo)")
plt.title("Box Plot of Luminosity(L/Lo)")
plt.show()