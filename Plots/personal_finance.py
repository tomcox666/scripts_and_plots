import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Read the CSV file into a DataFrame
df = pd.read_csv("../plot_data/A37W_personal_financial_2020.csv")

monetary_columns = ['Savings($)', 'Stocks($)', 'Bonds($)', 'Travel Expense($)', 'Home Renovation($)', 'Credit Card Debt($)']
for col in monetary_columns:
    df[col] = df[col].str.replace(',', '').str.replace('$', '').astype(float)

# Replace NaN values with zero
df.fillna(0, inplace=True)

# Forward-fill 0 values
df.replace(0, method='bfill', inplace=True)

# Convert the 'Date' column to datetime (assuming it's in 'YYYY-MM-DD' format)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Create line plots for Income, Expense, and Savings
plt.figure(figsize=(12, 6))

# Plot historical data
plt.scatter(df['Date'], df['Income($)'], marker='o', label='Income (Historical)')
plt.scatter(df['Date'], df['Expense($)'], marker='o', label='Expense (Historical)')
plt.scatter(df['Date'], df['Savings($)'], marker='o', label='Savings (Historical)')

# Fit ARIMA models for Income, Expense, and Savings
for col in ['Income($)', 'Expense($)', 'Savings($)']:
    model = ARIMA(df[col], order=(7, 3, 2))
    model_fit = model.fit()

    # Extend forecast dates to cover the forecast period
    forecast_dates = pd.date_range(start=df['Date'].max(), periods=7, freq='MS')
    forecast_y = model_fit.forecast(steps=7)

    # Plot the extended projection line
    plt.plot(forecast_dates, forecast_y, label=f'{col} (Forecasted)')

plt.xlabel('Date')
plt.ylabel('Amount ($)')
plt.title('Income, Expense, and Savings Over Time')
plt.legend()

plt.grid(True)
plt.tight_layout()

plt.show()