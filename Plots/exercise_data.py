import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Read the CSV file into a DataFrame
df = pd.read_csv("../plot_data/ZGNX_running_by_week - ZGNX_running_by_week.csv")

# Remove the last row, this is a summary row
df = df.drop(df.index[-1])

# Function to strip commas from values in a DataFrame
def strip_commas(df):
    for col in df.columns:
        if df[col].dtype == object:  # Only process columns with object (string) dtype
            df[col] = df[col].str.replace(',', '')
    return df

# Strip commas from all values in the DataFrame
df = strip_commas(df)

# Clean and convert data to numerical format
df['Total Distance'] = df['Total Distance'].str.replace(' mi', '').astype(float)
df['Average Distance'] = df['Average Distance'].str.replace(' mi', '').astype(float)
df['Max Distance'] = df['Max Distance'].str.replace(' mi', '').astype(float)

df['Total Activity Time'] = df['Total Activity Time'].str.extract('(\d+:\d+:\d+)', expand=False)  # Extract only the 'hh:mm:ss' format
df['Total Activity Time'] = pd.to_timedelta(df['Total Activity Time'], errors='coerce')  # Convert to timedelta

df['Activity Calories'] = df['Activity Calories'].astype(int)
df['Total Ascent'] = df['Total Ascent'].str.replace(' ft', '').astype(int)
df['Avg Ascent'] = df['Avg Ascent'].str.replace(' ft', '').astype(int)
df['Max Ascent'] = df['Max Ascent'].str.replace(' ft', '').astype(int)
df['Total Descent'] = df['Total Descent'].str.replace(' ft', '').astype(int)
df['Avg Descent'] = df['Avg Descent'].str.replace(' ft', '').astype(int)
df['Max Descent'] = df['Max Descent'].str.replace(' ft', '').astype(int)
df['Average Heart Rate'] = df['Average Heart Rate'].str.replace(' bpm', '').astype(int)
df['Max Heart Rate'] = df['Max Heart Rate'].str.replace(' bpm', '').astype(int)
df['Average Run Cadence'] = df['Average Run Cadence'].str.replace(' spm', '').astype(int)
df['Max Run Cadence'] = df['Max Run Cadence'].str.replace(' spm', '').astype(int)
df['Average Stride Length'] = df['Average Stride Length'].str.replace(' m', '').astype(float)

# Exploratory Analysis

# Distribution Plots
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
sns.histplot(df['Total Distance'], bins=20, kde=True)
plt.title('Total Distance')

plt.subplot(1, 3, 2)
sns.histplot(df['Average Distance'], bins=20, kde=True)
plt.title('Average Distance')

plt.subplot(1, 3, 3)
sns.histplot(df['Max Distance'], bins=20, kde=True)
plt.title('Max Distance')

plt.tight_layout()
plt.show()

# Time Series Plot
plt.figure(figsize=(12, 6))
plt.plot(df['Time Period'], df['Total Distance'], label='Total Distance')
plt.plot(df['Time Period'], df['Activities'], label='Activities')
plt.plot(df['Time Period'], df['Total Activity Time'].dt.total_seconds() / 3600, label='Total Activity Time (hours)')
plt.xlabel('Time Period')
plt.ylabel('Values')
plt.title('Time Series Plot')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Correlation Matrix
# Convert 'Average Pace' and 'Avg Grade-Adjusted Pace' to numeric, handle errors
df['Average Pace'] = pd.to_numeric(df['Average Pace'].str.replace(' /mi', ''), errors='coerce')
df['Avg Grade-Adjusted Pace'] = pd.to_numeric(df['Avg Grade-Adjusted Pace'].str.replace(' /mi', ''), errors='coerce')

correlation_columns = ['Total Distance', 'Average Distance', 'Max Distance', 'Total Activity Time',
                       'Activity Calories', 'Average Heart Rate', 'Max Heart Rate', 'Total Ascent', 'Total Descent',
                       'Average Pace', 'Avg Grade-Adjusted Pace']

correlation_matrix = df[correlation_columns].corr()

# Display the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()