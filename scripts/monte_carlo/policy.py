import numpy as np

# Define the behavior policy function (e.g., random policy)
def random_policy(state):
    num_actions = 2  # Assuming there are only two actions available: hit or stick
    return np.ones(num_actions) / num_actions  # Return equal probabilities for each action
