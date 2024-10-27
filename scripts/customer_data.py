import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import sys
import os

def load_data(filepath):
    """Loads customer purchase data from a CSV file, handling errors."""
    try:
        if not filepath.lower().endswith('.csv'):
            raise ValueError("File must be a CSV file.")
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found at {filepath}")
        df = pd.read_csv(filepath)
        if not {'CustomerID', 'ProductID', 'PurchaseAmount'}.issubset(df.columns):
            raise ValueError("CSV file must contain 'CustomerID', 'ProductID', and 'PurchaseAmount' columns.")
        if df.isnull().values.any():
        
            df.fillna(0, inplace=True)  # Handle missing values by filling them with zeros. Alternative methods such as mean imputation could be used instead.
        return df
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        sys.exit(1)

def preprocess_data(df):
    """Preprocesses the data for clustering."""
    customer_product_matrix = df.pivot_table(index='CustomerID', columns='ProductID', values='PurchaseAmount', fill_value=0)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(customer_product_matrix)
    return scaled_data

def perform_kmeans(data, n_clusters=4, max_iter=300, n_init=10):
    """Performs K-means clustering with optimization."""
    try:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=n_init, max_iter=max_iter, algorithm='lloyd')
        kmeans.fit(data)
        return kmeans
    except Exception as e:
        print(f"Error performing K-means clustering: {e}")
        sys.exit(1)

def visualize_clusters(data, kmeans):
    """Visualizes the clusters using PCA."""
    try:
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(data)
        plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=kmeans.labels_, cmap='viridis')
        plt.title('Customer Clusters')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.show()
    except Exception as e:
        print(f"Error visualizing clusters: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    df = load_data(filepath)
    scaled_data = preprocess_data(df)
    kmeans = perform_kmeans(scaled_data)  # Using default optimized parameters
    visualize_clusters(scaled_data, kmeans)