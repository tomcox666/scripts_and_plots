import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("~/data_annotation/plot_data/EX97_stars.csv")

# Display the first 5 rows
print(df.head())

# Get information about the columns and their data types
print(df.info())

# Extract the data for the plot
temperature = df["Temperature (K)"]
radius = df["Radius(R/Ro)"]

# Create the scatter plot
plt.figure()
plt.scatter(temperature, radius)

# Label and display the plot
plt.xlabel("Temperature (K)")
plt.ylabel("Radius (R/Ro)")
plt.title("Relationship between Temperature and Radius of Stars")
plt.show()