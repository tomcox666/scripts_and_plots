import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Function to generate synthetic financial data for each week
def generate_financial_data(start_date, num_weeks, starting_income, income_growth_rate):
    dates = pd.date_range(start=start_date, periods=num_weeks, freq='W')  # Weekly data
    
    # Initialize lists for financial metrics
    income = []
    expenses = []
    savings = []
    stocks = []
    bonds = []
    real_estate = []
    travel_expense = []
    home_renovation = []
    credit_card_debt = []
    
    # Initial values for financial variables
    current_income = starting_income
    current_savings = 1000  # Starting savings
    current_stocks = 5000
    current_bonds = 2000
    current_real_estate = 10000
    current_credit_card_debt = 500
    
    for i in range(num_weeks):
        # Simulate income growth over time
        current_income += current_income * income_growth_rate
        
        # Simulate expenses as a portion of income with some randomness
        expense = current_income * random.uniform(0.4, 0.7)
        
        # Savings is what's left after expenses
        saving = current_income - expense
        
        # Stocks and bonds grow by a small percentage with randomness
        current_stocks += current_stocks * random.uniform(-0.02, 0.05)  # Stocks may increase or decrease
        current_bonds += current_bonds * random.uniform(0.01, 0.03)  # Bonds are more stable
        
        # Real estate grows slowly, if at all
        current_real_estate += current_real_estate * random.uniform(0.005, 0.02)
        
        # Check for market crash: simulate a drop in value
        if random.random() < 0.05:  # 5% chance every week
            drop_percentage = 0.20  # 20% drop during a crash
            current_stocks *= (1 - drop_percentage)
            current_bonds *= (1 - drop_percentage)  # Optionally apply drop to bonds
            current_real_estate *= (1 - drop_percentage)  # Optionally apply drop to real estate
        
        # Random travel or home renovation expenses (may not occur every week)
        travel = random.uniform(0, 300) if random.random() < 0.1 else 0
        renovation = random.uniform(0, 500) if random.random() < 0.05 else 0
        
        # Credit card debt can fluctuate with expenses
        current_credit_card_debt += random.uniform(-100, 200)
        current_credit_card_debt = max(current_credit_card_debt, 0)  # Debt can't be negative
        
        # Append values to lists
        income.append(round(current_income, 2))
        expenses.append(round(expense + travel + renovation, 2))
        savings.append(round(saving, 2))
        stocks.append(round(current_stocks, 2))
        bonds.append(round(current_bonds, 2))
        real_estate.append(round(current_real_estate, 2))
        travel_expense.append(round(travel, 2))
        home_renovation.append(round(renovation, 2))
        credit_card_debt.append(round(current_credit_card_debt, 2))
    
    # Create a DataFrame from the lists
    data = pd.DataFrame({
        'Date': dates,
        'Income($)': income,
        'Expense($)': expenses,
        'Savings($)': savings,
        'Stocks($)': stocks,
        'Bonds($)': bonds,
        'Real Estate($)': real_estate,
        'Travel Expense($)': travel_expense,
        'Home Renovation($)': home_renovation,
        'Credit Card Debt($)': credit_card_debt
    })
    
    return data

# Generate 3 years of weekly data (3 * 52 weeks)
num_years = 5
num_weeks = num_years * 52

# Starting parameters
starting_income = 3000  # Initial income in dollars
income_growth_rate = 0.01  # Income grows by 1% each week

# Generate financial data
financial_data = generate_financial_data(start_date="2002-01-01", num_weeks=num_weeks, starting_income=starting_income, income_growth_rate=income_growth_rate)

# Save the data to a CSV file
financial_data.to_csv('expanded_financial_data_with_crash.csv', index=False)

print("Generated financial data with market crash simulation saved to 'expanded_financial_data_with_crash.csv'")
