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


# Define a dictionary to map colors to color codes
color_mapping = {
    'Red': 'red',
    'Blue': 'blue',
    'Bluew Wite': 'lightblue',  # Assuming a light shade of blue
    'White': 'white',
    'Yellowish White': 'yellow',
    'Whitish': 'lightgray',    # Assuming a light shade of gray
    'Pale yellow orange': 'lightyellow',
    'Orange': 'orange',
    'White-yellow': 'lightyellow',  # Assuming a light shade of yellow
    'Yellow-white': 'lightyellow',  # Assuming a light shade of yellow
    'Blue-white': 'lightblue',       # Assuming a light shade of blue
    'Orange-red': 'orangered'        # Assuming a shade of orange-red
}

# Map the color strings to color codes
colors = df["Star color"].map(color_mapping).fillna('gray')

# Plot the scatter plot with the mapped colors
plt.scatter(df["Temperature (K)"], df["Luminosity(L/Lo)"], c=colors)

# Label the axes
plt.xlabel("Temperature (K)")
plt.ylabel("Luminosity(L/Lo)")

# Add a title
plt.title("Relationship Between Temperature and Luminosity")

# Show the plot
plt.show()