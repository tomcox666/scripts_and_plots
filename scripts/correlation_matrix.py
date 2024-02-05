import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Import data
data = pd.read_csv('~/data_annotation/plot_data/Netflix_TV_Shows_and_Movies.csv')
column1 = 'Temperature (Celsius)'
column2 = 'Precipitation (mm)'


#data.drop('Year', axis=1, inplace=True)  # drop the Year column
correlation_matrix = data.corr()

# Plot the correlation matrix using Seaborn for better visualization
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap=plt.get_cmap('YlGnBu'), square=True)

# Add axis labels and a title
plt.title('Correlation Matrix of Environmental Variables', fontsize=14)

# Customize the colorbar
cbar = heatmap.collections[0].colorbar
cbar.set_label('Correlation Coefficient', fontsize=12)
cbar.ax.tick_params(labelsize=10)

# Adjust layout to prevent cutoff of axis labels
plt.tight_layout()

# Show the plot
plt.show()