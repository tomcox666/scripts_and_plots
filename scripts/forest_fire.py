import json
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from perlin_noise import PerlinNoise

# Load parameters from JSON
with open('fire_config.json', 'r') as f:
    config = json.load(f)

forest_size = config['forest_size']
tree_density = config['tree_density']
lake_frequency = config['lake_frequency']
river_probability = config['river_probability']
fire_spread_probability = config['fire_spread_probability']
spread_over_gap_probability = config['spread_over_gap_probability']
wind_speed = config['wind']['speed']
wind_direction = config['wind']['direction']
maximum_steps = config['maximum_steps']

# Terrain types
EMPTY = 0
TREE = 1
FIRE = 2
WATER = 3

# Initialize forest grid with Perlin noise for terrain variation
noise = PerlinNoise(octaves=3)
forest = np.zeros((forest_size, forest_size))
for x in range(forest_size):
    for y in range(forest_size):
        noise_val = noise([x/forest_size, y/forest_size])
        if noise_val > 0.25 - (0.25 * tree_density):
            forest[x, y] = TREE
        elif noise_val > -0.25 - (0.25 * lake_frequency / 10):
            forest[x, y] = EMPTY
        else:
            forest[x, y] = WATER
        if random.random() < river_probability * 0.01:
            forest[x, y] = WATER
            for i in range(random.randint(3, 10)):
                if x+i < forest_size:
                    forest[x+i, y] = WATER

# Find a suitable starting point for the fire (a tree cell)
start_x, start_y = forest_size // 2, forest_size // 2
while forest[start_x, start_y] != TREE:
    start_x, start_y = random.randint(0, forest_size-1), random.randint(0, forest_size-1)
forest[start_x, start_y] = FIRE

# Wind direction mapping
wind_offsets = {
    "N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0),
    "NE": (1, -1), "SE": (1, 1), "SW": (-1, 1), "NW": (-1, -1)
}
dx, dy = wind_offsets.get(wind_direction, (0, 0))

# Simulation steps
frames = []
for _ in range(maximum_steps):
    frames.append(np.copy(forest))
    new_forest = np.copy(forest)
    for x in range(forest_size):
        for y in range(forest_size):
            if forest[x, y] == FIRE:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0: continue
                        if 0 <= x + i < forest_size and 0 <= y + j < forest_size:
                            spread_prob = fire_spread_probability
                            if (i == dx and j == dy): spread_prob = min(1, fire_spread_probability + 0.2)
                            elif (i == -dx and j == -dy): spread_prob = max(0, fire_spread_probability - 0.2)
                            if forest[x + i, y + j] == TREE and random.random() < spread_prob:
                                new_forest[x + i, y + j] = FIRE
                            elif forest[x + i, y + j] == EMPTY and random.random() < spread_over_gap_probability:
                                new_forest[x + i, y + j] = FIRE
                new_forest[x, y] = EMPTY
    forest = new_forest
    if np.sum(forest == FIRE) == 0:
        break

# Visualization
fig, ax = plt.subplots()
cmap = plt.cm.colors.ListedColormap(['white', 'green', 'red', 'blue'])
im = ax.imshow(frames[0], animated=True, cmap=cmap)
ax.set_title("Forest Fire Simulation")
legend_elements = [
    plt.Line2D([0], [0], marker='s', color='w', label='Empty', markerfacecolor='white', markersize=10),
    plt.Line2D([0], [0], marker='s', color='w', label='Forest', markerfacecolor='green', markersize=10),
    plt.Line2D([0], [0], marker='s', color='w', label='Fire', markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='s', color='w', label='Water', markerfacecolor='blue', markersize=10)
]
ax.legend(handles=legend_elements, loc='upper right')

# Corrected lambda function for animation
def update(frame):
    im.set_array(frames[frame])
    return [im]

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=50, blit=True)
plt.show()