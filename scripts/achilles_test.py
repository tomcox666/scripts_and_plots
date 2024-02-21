import pandas as pd

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("../plot_data/current_accounts.csv")

# Visualize the trends (bar/stacked bar chart)
import matplotlib.pyplot as plt

voucher_counts = df['Voucher Type'].value_counts()

voucher_counts.plot(kind='bar',colormap='Set3')
plt.xlabel('Expiration Group')
plt.ylabel('Voucher Count')
plt.title('Distribution of Voucher Types by Supplier and Expiration')
plt.legend(title='Voucher Type')
plt.show()


# Display processed data information
print("'Updated data:")
df.info()