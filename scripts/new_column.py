import numpy as np
import pandas as pd

# Define the function add_correlated_column from Response A
def add_correlated_column(df, col_name, corr_value):
    """
    Adds a new column to the DataFrame with a random variable correlated with the specified column.

    Args:
        df: The DataFrame to add the column to.
        col_name: The name of the column to correlate with.
        corr_value: The desired correlation value.

    Returns:
        The DataFrame with the new column added.
    """

    # Calculate the standard deviation of the existing column
    std_dev = df[col_name].std()

    # Generate random numbers with the desired correlation
    mean = 0
    cov = [[std_dev**2, corr_value * std_dev**2], [corr_value * std_dev**2, std_dev**2]]
    random_numbers = np.random.multivariate_normal([mean, mean], cov, df.shape[0])

    # Add the new column to the DataFrame
    df['new_column'] = random_numbers[:, 1]

    return df

def main():
    # Create a sample dataset
    np.random.seed(0)  # For reproducibility
    num_rows = 100
    dataset = pd.DataFrame({
        'ID': np.random.randint(1, 10, num_rows),
        'AMT': np.random.uniform(100, 1000, num_rows),
        'TIME': np.random.randint(1, 24, num_rows),
        'DV': np.random.randint(0, 2, num_rows),
        'CMT': np.random.choice(['A', 'B', 'C'], num_rows),
        'MDV': np.random.randint(0, 2, num_rows),
        'RATE': np.random.uniform(0.5, 2.0, num_rows),
        'BWT_Norm': np.random.normal(0, 1, num_rows)
    })

    # Display the original dataset
    print("Original Dataset:")
    print(dataset.head())

    # Add a new column with correlated random values
    dataset_with_new_column = add_correlated_column(dataset, 'BWT_Norm', 0.5)

    # Display the dataset with the new column
    print("\nDataset with New Correlated Column:")
    print(dataset_with_new_column.head())

if __name__ == "__main__":
    main()