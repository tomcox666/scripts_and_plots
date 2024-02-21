import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../plot_data/Wine InventorySheet1.csv')

df.sort_values(['Profit'], ascending=False, inplace=True)
print(df[['Wine Name', 'Profit']].groupby('Wine Name').mean())

wine_name_list = df['Wine Name'].unique()

for wine_name in wine_name_list:
    wine_df = df[df['Wine Name'] == wine_name]
    plt.scatter(x=wine_df['Price ($)'], y=wine_df['Sold'], label=wine_name)

wine_name_list = df['Wine Name'].unique()

for wine_name in wine_name_list:
    wine_df = df[df['Wine Name'] == wine_name]
    plt.scatter(x=wine_df['Price ($)'], y=wine_df['Profit'], label=wine_name)
plt.legend()
plt.show()