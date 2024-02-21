import numpy as np
import pandas as pd

# Define the WebGraph class
class WebGraph:
    def __init__(self, adj_matrix, damping_factor=0.85):
        self.adj_matrix = adj_matrix
        self.n = len(adj_matrix)
        self.damping_factor = damping_factor
        self.page_scores = np.ones(self.n) / self.n

    def update_page_scores(self):
        new_page_scores = (1 - self.damping_factor) / self.n + self.damping_factor * self.adj_matrix.T.dot(self.page_scores)
        self.page_scores = new_page_scores

    def get_page_ranks(self, max_iter=100, convergence_threshold=0.001):
        for i in range(max_iter):
            old_page_scores = self.page_scores.copy()
            self.update_page_scores()
            delta = np.abs(self.page_scores - old_page_scores).sum()
            if delta <= convergence_threshold:
                break
        return self.page_scores

# Example usage:
# Create a transition matrix
adj_matrix = np.array([[0, 1/2, 1/2, 0, 0],
                       [1/3, 0, 0, 0, 2/3],
                       [1/2, 0, 0, 1/2, 0],
                       [0, 0, 1/3, 0, 2/3],
                       [1/2, 1/2, 0, 0, 0]])

# Initialize the WebGraph object
web_graph = WebGraph(adj_matrix)

# Calculate page ranks
page_ranks = web_graph.get_page_ranks()

# Convert page ranks to a DataFrame
df = pd.DataFrame({'Page': ['A', 'B', 'C', 'D', 'E'], 'Page Rank': page_ranks}).sort_values('Page Rank', ascending=False)

# Print the results
print(df)