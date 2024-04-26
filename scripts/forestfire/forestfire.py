import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

def initialize_forest(size, density, firebreak_freq, firebreak_width):
    forest = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if np.random.rand() < density:
                forest[i][j] = 1  # Tree
            if (i % firebreak_freq == 0 or j % firebreak_freq == 0) and np.random.rand() < firebreak_width:
                forest[i][j] = -1  # Firebreak
    return forest

def simulate_fire(forest, fire_prob, wind_speed, wind_dir, firebreak_prob, spread_over_gap_prob, max_steps):
    size = forest.shape[0]
    fire_progress = []

    # Start the fire in the center
    mid = size // 2
    forest[mid][mid] = 2

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    if wind_dir.lower() in ["n", "north"]:
        wind_offset = (-1, 0)
    elif wind_dir.lower() in ["e", "east"]:
        wind_offset = (0, 1)
    elif wind_dir.lower() in ["s", "south"]:
        wind_offset = (1, 0)
    elif wind_dir.lower() in ["w", "west"]:
        wind_offset = (0, -1)
    else:
        wind_offset = (0, 0)

    for _ in range(max_steps):
        new_forest = np.copy(forest)
        for i in range(size):
            for j in range(size):
                if forest[i][j] == 2:  # Burning
                    new_forest[i][j] = 3  # Burning -> ash
                    for dx, dy in directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < size and 0 <= nj < size:
                            if new_forest[ni][nj] != 1:  # If not a tree, skip
                                continue
                            prob = fire_prob
                            if wind_speed > 0:
                                if (ni - i) * wind_offset[0] > 0 or (nj - j) * wind_offset[1] > 0:
                                    prob += wind_speed * 0.3
                            if np.random.rand() < prob:
                                new_forest[ni][nj] = 2  # Tree catches fire

        fire_progress.append(new_forest)
        if np.all(new_forest != 2):
            break
        forest = new_forest

    return fire_progress

def visualize_fire(fire_progress, wind_speed, wind_dir):
    fig, ax = plt.subplots()
    cmap = ListedColormap(["gray", "white", "green", "red", "black"])
    norm = plt.Normalize(-1, 3)

    def update(frame):
        ax.clear()
        ax.set_title(f"Step {frame} - Wind: {wind_speed} mph {wind_dir}")
        ax.imshow(fire_progress[frame], interpolation="nearest", cmap=cmap, norm=norm)
        ax.axis("off")

    ani = animation.FuncAnimation(
        fig, update, frames=len(fire_progress), repeat=False, interval=200
    )
    plt.show()

# Simulation parameters
size = 200
density = 0.6
fire_prob = 0.75
max_steps = 250 
firebreak_freq = 50 
firebreak_width = 0.8  
firebreak_prob = 1 
spread_over_gap_prob = 0.1  

wind_speed_input = input("Enter wind speed (mph) or press Enter for no wind: ")
wind_dir_input = input("Enter wind direction (N, E, S, W) or press Enter for no wind: ")

wind_speed = float(wind_speed_input) if wind_speed_input else 0
wind_dir = wind_dir_input.upper() if wind_dir_input else "None"

forest = initialize_forest(size, density, firebreak_freq, firebreak_width)
fire_progress = simulate_fire(forest, fire_prob, wind_speed, wind_dir, firebreak_prob, spread_over_gap_prob, max_steps)

visualize_fire(fire_progress, wind_speed, wind_dir)