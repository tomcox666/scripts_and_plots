# In test.py
from environment import BlackjackEnv
from functions import off_policy_mc_prediction_importance_sampling
from policy import random_policy

# Create environment instance
env = BlackjackEnv()

# Reset the environment to get the initial state
initial_state = env.reset()
print("Initial state:", initial_state)

# Take an action (e.g., hit) and observe the next state
action = 1  # Example action (hit)
next_state, reward, done, _ = env.step(action)
print("Next state:", next_state)

# Test the function by passing the behavior policy without calling it with arguments
V = off_policy_mc_prediction_importance_sampling(env, num_episodes=10000, behaviour_policy=random_policy, discount_factor=1.0)
print(V)
