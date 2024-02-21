
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('../plot_data/Woodworking Class Data.csv')

# Calculate descriptive statistics for numeric columns
df_numeric = df[['Number of participants', 'Price of class', 'Class gross income', 'Net profit for class']]
stats = df_numeric.describe()
print(stats.to_markdown())

# Calculate average number of participants, gross income, and net profit by class name
df_grouped = df.groupby('Class name')[['Number of participants', 'Class gross income', 'Net profit for class']].mean()
print(df_grouped.to_markdown())

# Create bar plot of average number of participants per class name
plt.bar(df_grouped.index, df_grouped['Number of participants'])
plt.xlabel('Class Name')
plt.ylabel('Average Number of Participants')
plt.title('Average Number of Participants per Class Name')
plt.show()

# Convert 'Date of class' to datetime format
df['Date of class'] = pd.to_datetime(df['Date of class'], format="%m/%d/%Y")

# Create line plot of class gross income trend over date of class
plt.plot(df['Date of class'], df['Class gross income'])
plt.xlabel('Date of Class')
plt.ylabel('Class Gross Income')
plt.title('Class Gross Income Trend over Date of Class')
plt.show()

# Convert class names to categorical variables
df['Class category'] = pd.Categorical(df['Class name'])
# Assign a unique color to each category
df['Color'] = df['Class category'].cat.codes

# Create scatter plot of net profit vs price, colored by class name
plt.scatter(df['Price of class'], df['Net profit for class'], c=df['Color'], cmap='viridis')
plt.xlabel('Price of Class')
plt.ylabel('Net Profit for Class')
plt.title('Net Profit for Class vs Price of Class')
plt.colorbar(label='Class')
plt.show()