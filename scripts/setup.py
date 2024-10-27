import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range (e.g., 30 days starting from today)
start_date = datetime.now()
date_range = [start_date - timedelta(days=x) for x in range(30)]

# Generate random values between 50 and 150
values = np.random.uniform(50, 150, size=len(date_range))

# Create a DataFrame with the generated data
data = pd.DataFrame({
    'Date': date_range,
    'Value': values
})

# Reverse the DataFrame so that dates go from past to present
data = data[::-1].reset_index(drop=True)

# Save the DataFrame to a CSV file
data.to_csv('data.csv', index=False)

print("Test data 'data.csv' has been created.")
