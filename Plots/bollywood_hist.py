import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file
file_path = "../plot_data/Top_1000_Bollywood_Movies.csv"
df = pd.read_csv(file_path)

# Plot histograms for Indian Gross and Indian Net
plt.figure(figsize=(12, 6))

# Histogram for Indian Gross
plt.subplot(1, 2, 1)
plt.hist(df['India Gross'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Indian Gross')
plt.xlabel('Indian Gross')
plt.ylabel('Frequency')

# Histogram for Indian Net
plt.subplot(1, 2, 2)
plt.hist(df['India Net'], bins=30, color='salmon', edgecolor='black')
plt.title('Distribution of Indian Net')
plt.xlabel('Indian Net')
plt.ylabel('Frequency')

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Plot histogram for Indian Gross
plt.hist(df['India Gross'], bins=30, color='skyblue', alpha=0.7, label='Indian Gross')
# Plot histogram for Indian Net
plt.hist(df['India Net'], bins=30, color='salmon', alpha=0.7, label='Indian Net')

plt.title('Distribution of Indian Gross and Indian Net')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()