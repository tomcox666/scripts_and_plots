import numpy as np
from collections import defaultdict
from policy import random_policy

def off_policy_mc_prediction_importance_sampling(env, num_episodes, behaviour_policy, discount_factor=1.0):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    C = defaultdict(lambda: np.zeros(env.action_space.n))
    target_policy = random_policy(Q)

    for i_episode in range(1, num_episodes + 1):
        episode = []
        state = env.reset()
        for i in range(100):
            probability = behaviour_policy(state)
            action = np.random.choice(np.arange(len(probability)), p=probability)
            next_state, reward, done, info = env.step(action)
            episode.append((state, action, reward))
            if done:
                break
            state = next_state

        G = 0.0
        W = 1.0

        for step in range(len(episode))[::-1]:
            state, action, reward = episode[step]
            G = discount_factor * G + reward
            C[state][action] += W
            Q[state][action] += (W / C[state][action]) * (G - Q[state][action])
            if action != np.argmax(target_policy(state)):
                break
            W = W * 1. / behaviour_policy(state)[action]

    return Q, target_policy