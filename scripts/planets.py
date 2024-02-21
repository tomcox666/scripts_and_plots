import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("../plot_data/X89N_planets - X89N_planets.csv")

df = df.drop(columns=['planet', 'planet_type'])
# Calculate the correlation matrix
corr_matrix = df.corr()

# Focus on columns with missing values
columns_with_missing = df.columns[df.isnull().any()]

# Create a heatmap of correlations
heatmap = sns.heatmap(corr_matrix[columns_with_missing], annot=True, cmap='coolwarm')
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45)
plt.title("Heatmap of Correlations (Focusing on Missing Values)")
plt.show() 