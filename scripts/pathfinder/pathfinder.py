import heapq
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.animation as animation
from noise import pnoise2, snoise2

# Define the Node class for pathfinding algorithms
class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g  # Cost from start to this node
        self.h = h  # Heuristic cost from this node to goal
        self.f = g + h  # Total cost
        self.parent = parent  # Parent node to trace back the path

    def __lt__(self, other):
        return self.f < other.f

terrain_costs = {
    0: 1,    # Open space
    1: 10,   # Forest
    2: 50,   # Water
    3: 80,   # Mountain (faster than before)
    4: 5,    # Swamp
    5: 150,  # Lava
}

# Define terrain speeds in km/h (flat ground)
terrain_speeds = {
    0: 5,    # Open space
    1: 4.5,  # Forest (50% slower than open space)
    2: 1,    # Water (20% of open space speed)
    3: 4,    # Mountain (slightly faster when flat)
    4: 2.25, # Swamp (25% slower than open space)
    5: 0.01   # Lava (2% of open space speed)
}

# Define a base multiplier for gradient effect
gradient_multiplier = 0.8

def calculate_path_time(path, grid, terrain_heights):
    total_time = 0
    for i in range(len(path) - 1):
        current_pos = path[i]
        next_pos = path[i + 1]
        terrain_type = grid[next_pos[0]][next_pos[1]]
        height_diff = abs(terrain_heights[next_pos[0]][next_pos[1]] - terrain_heights[current_pos[0]][current_pos[1]])
        distance = np.linalg.norm(np.array(next_pos) - np.array(current_pos))
        speed = terrain_speeds[terrain_type] * (1 - height_diff / 100) * gradient_multiplier
        time = distance / speed
        total_time += time
    return total_time

# A* heuristic function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

# A* Algorithm implementation
def astar(grid, start, goal):
    open_list = []
    closed_list = set()
    
    start_node = Node(start)
    goal_node = Node(goal)
    
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        closed_list.add(current_node.position)
        
        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Reverse to get the correct order
        
        (x, y) = current_node.position
        neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        
        for next_pos in neighbors:
            # Check if the position is valid and not in closed list
            if (
                0 <= next_pos[0] < len(grid)
                and 0 <= next_pos[1] < len(grid[0])
                and next_pos not in closed_list
            ):
                terrain_cost = terrain_costs[grid[next_pos[0]][next_pos[1]]]
                new_g = current_node.g + terrain_cost  
                
                # Penalty based on terrain 'danger' (avoids costly terrain types)
                if terrain_cost >= 50: 
                    h = heuristic(next_pos, goal_node.position) * 1.5  # Inflate heuristic 
                else:
                    h = heuristic(next_pos, goal_node.position) 
                    
                new_node = Node(next_pos, new_g, h, current_node)
                
                already_in_open_list = False
                for open_node in open_list:
                    if (
                        open_node.position == new_node.position
                        and open_node.f <= new_node.f
                    ):
                        already_in_open_list = True
                        break
                if not already_in_open_list:
                    heapq.heappush(open_list, new_node)
    
    return None  # If no valid path is found

# Dijkstra's Algorithm implementation 
def dijkstra(grid, start, goal):
    distances = [[float("inf") for _ in range(len(grid[0]))] for _ in range(len(grid))]
    distances[start[0]][start[1]] = 0

    pq = [(0, start)]  # Priority queue with (distance, position) pairs

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node == goal:
            # Backtrace to find the path
            path = []
            while current_node:
                path.append(current_node)
                current_node = find_previous(distances, grid, current_node)
            return path[::-1]  # Reverse to get the correct order

        (x, y) = current_node
        neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

        for neighbor in neighbors:
            if (
                0 <= neighbor[0] < len(grid)
                and 0 <= neighbor[1] < len(grid[0])
                and distances[neighbor[0]][neighbor[1]] > current_dist + terrain_costs[grid[neighbor[0]][neighbor[1]]]
            ):
                terrain_cost = terrain_costs[grid[neighbor[0]][neighbor[1]]]
                new_distance = current_dist + terrain_cost

                if new_distance < distances[neighbor[0]][neighbor[1]]:
                    distances[neighbor[0]][neighbor[1]] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))
    
    return None  # If no valid path is found

# Helper function to backtrack the path in Dijkstra's
def find_previous(distances, grid, current_node):
    (x, y) = current_node
    neighbors = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]

    best_neighbor = None
    for neighbor in neighbors:
        if (
            0 <= neighbor[0] < len(grid)
            and 0 <= neighbor[1] < len(grid[0])
            and distances[neighbor[0]][neighbor[1]] < distances[x][y]
        ):
            if best_neighbor is None or distances[neighbor[0]][neighbor[1]] < distances[x][y]:
                best_neighbor = neighbor

    return best_neighbor

"""def visualize_paths(grid, start, goal, paths):
    num_paths = len(paths)

    # Titles for each subplot
    titles = ["A* Path", "Dijkstra Path"]

    fig, axes = plt.subplots(1, num_paths, figsize=(12, 6), sharex=True, sharey=True)

    if not isinstance(axes, (list, np.ndarray)):
        axes = [axes]

    # Color mapping for terrain
    color_dict = {
        0: [154, 205, 50],  # Open space: yellowgreen
        1: [34, 139, 34],   # Forest: forest green
        2: [0, 0, 255],     # Water: blue
        3: [128, 128, 128],  # Mountain: grey
        4: [205, 133, 63],  # Swamp
        5: [255, 140, 0],   # Lava
    }

    # Normalize RGB values
    for k, v in color_dict.items():
        color_dict[k] = [x / 255 for x in v]

    # Define terrain types and their corresponding speeds
    terrain_types = ["Open Space", "Forest", "Water", "Mountain", "Swamp", "Lava"]
    terrain_colors = [color_dict[i] for i in range(6)]
    terrain_speeds_str = [f"{terrain_speeds[i]:.2f} km/h" for i in range(6)]

    # Create legend handles for each terrain type with its color
    legend_handles = [Patch(facecolor=terrain_colors[i], label=f"{terrain_types[i]} ({terrain_speeds_str[i]})") for i in range(6)]

    for ax, path, title in zip(axes, paths, titles):
        # Plot the terrain in each subplot
        grid_img = np.zeros((grid.shape[0], grid.shape[1], 3))
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                grid_img[i, j] = color_dict[grid[i, j]]

        ax.imshow(grid_img)

        ax.scatter(start[1], start[0], marker="o", color="blue", s=80, label="Start")
        ax.scatter(goal[1], goal[0], marker="s", color="red", s=80, label="Goal")
        ax.set_title(f"{title}")  # Add title to each subplot
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")

        # Add legend with terrain types
        ax.legend(title="Terrain Types", handles=legend_handles)

    # Initialize the line objects
    lines = []
    for ax, path in zip(axes, paths):
        line, = ax.plot([], [], color="lime", linewidth=3)
        lines.append(line)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for line, path in zip(lines, paths):
            path_x = [p[1] for p in path[:i]]  # x-coordinates
            path_y = [p[0] for p in path[:i]]  # y-coordinates
            line.set_data(path_x, path_y)
        return lines

    ani = animation.FuncAnimation(fig, animate, frames=len(paths[0]), init_func=init, blit=True, interval=50)

    plt.tight_layout()
    plt.show()"""

def visualize_paths(grid, start, goal, paths):
    num_paths = len(paths)

    # Titles for each subplot
    titles = ["A* Path", "Dijkstra Path"]

    fig, axes = plt.subplots(1, num_paths, figsize=(12, 6), sharex=True, sharey=True, subplot_kw={'projection': '3d'})

    if not isinstance(axes, (list, np.ndarray)):
        axes = [axes]

    # Color mapping for terrain
    color_dict = {
        0: [154, 205, 50],  # Open space: yellowgreen
        1: [34, 139, 34],   # Forest: forest green
        2: [0, 0, 255],     # Water: blue
        3: [128, 128, 128],  # Mountain: grey
        4: [205, 133, 63],  # Swamp
        5: [255, 140, 0],   # Lava
    }

    # Normalize RGB values
    for k, v in color_dict.items():
        color_dict[k] = [x / 255 for x in v]

    # Define terrain types and their corresponding speeds
    terrain_types = ["Open Space", "Forest", "Water", "Mountain", "Swamp", "Lava"]
    terrain_colors = [color_dict[i] for i in range(6)]
    terrain_speeds_str = [f"{terrain_speeds[i]:.2f} km/h" for i in range(6)]

    # Create legend handles for each terrain type with its color
    legend_handles = [Patch(facecolor=terrain_colors[i], label=f"{terrain_types[i]} ({terrain_speeds_str[i]})") for i in range(6)]

    for ax, path, title in zip(axes, paths, titles):
        # Plot the terrain in each subplot
        grid_img = np.zeros((grid.shape[0], grid.shape[1], 3))
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                grid_img[i, j] = color_dict[grid[i, j]]

        x = np.arange(grid.shape[1])
        y = np.arange(grid.shape[0])
        X, Y = np.meshgrid(x, y)
        Z = terrain_heights

        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=grid_img, linewidth=0, antialiased=False)

        ax.scatter(start[1], start[0], terrain_heights[start[0], start[1]], marker="o", color="blue", s=80, label="Start")
        ax.scatter(goal[1], goal[0], terrain_heights[goal[0], goal[1]], marker="s", color="red", s=80, label="Goal")
        ax.set_title(f"{title}")  # Add title to each subplot
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")

        # Add legend with terrain types
        ax.legend(title="Terrain Types", handles=legend_handles)

    # Initialize the line objects
    lines = []
    for ax, path in zip(axes, paths):
        line, = ax.plot([], [], [], color="lime", linewidth=3)
        lines.append(line)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for line, path in zip(lines, paths):
            path_x = [p[1] for p in path[:i]]  # x-coordinates
            path_y = [p[0] for p in path[:i]]  # y-coordinates
            path_z = [terrain_heights[p[0], p[1]] for p in path[:i]]  # z-coordinates
            line.set_data(path_x, path_y)
            line.set_3d_properties(path_z)
        return lines

    ani = animation.FuncAnimation(fig, animate, frames=len(paths[0]), init_func=init, blit=True, interval=50, repeat=False)

    plt.tight_layout()
    plt.show(block=True)

def create_terrain_grid(grid_size, start, sigma=10, open_radius=3, swamp_threshold=0.6, max_swamp_distance=12):
    # Define noise parameters
    octaves = 4
    persistence = 0.2
    lacunarity = 4.0
    scale = 200.0

    # Generate Perlin noise and Gaussian gradient
    noise_grid = np.zeros(grid_size)
    gaussian_grid = np.zeros(grid_size)

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            noise_grid[i, j] = pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            distance = np.linalg.norm(np.array([i, j]) - np.array(start))
            gaussian_grid[i, j] = np.exp(-(distance ** 2) / (2 * sigma ** 2))

    # Blend Perlin noise with Gaussian gradient to focus open terrain near start
    focused_noise_grid = noise_grid * (1 - gaussian_grid)

    # Normalize the blended noise values to the range [0, 1]
    focused_noise_grid = (focused_noise_grid - focused_noise_grid.min()) / (focused_noise_grid.max() - focused_noise_grid.min())

    # Convert noise values to terrain types and heights
    terrain_grid = np.zeros(grid_size, dtype=int)
    terrain_heights = np.zeros(grid_size)

    # Helper function to check if a cell is near water
    def is_near_water(x, y):
        neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        return any(
            0 <= nx < grid_size[0] and 0 <= ny < grid_size[1] and terrain_grid[nx][ny] == 2
            for nx, ny in neighbors
        )

    # Helper function to propagate swamp with distance control
    def propagate_swamp(x, y, visited, distance):
        if (
            (x, y) in visited
            or not (0 <= x < grid_size[0] and 0 <= y < grid_size[1])
            or distance <= 0
        ):
            return

        visited.add((x, y))  # Mark the cell as visited
        if random.random() < swamp_threshold:
            terrain_grid[x, y] = 4  # Assign swamp

        # Propagate in all four directions, decrementing the distance
        propagate_swamp(x - 1, y, visited, distance - 1)
        propagate_swamp(x + 1, y, visited, distance - 1)
        propagate_swamp(x, y - 1, visited, distance - 1)
        propagate_swamp(x, y + 1, visited, distance - 1)

    # Initialize set to track visited cells for swamp propagation
    visited_cells = set()

    for i in range(grid_size[0]):
        for j in range (grid_size[1]):
            terrain_heights[i, j] = 100 * focused_noise_grid[i, j]

            if terrain_heights[i, j] < 20:
                terrain_grid[i, j] = 2  # Water
                # Propagate swamps within a certain distance from water
                propagate_swamp(i - 1, j, visited_cells, max_swamp_distance)
                propagate_swamp(i + 1, j, visited_cells, max_swamp_distance)
                propagate_swamp(i, j - 1, visited_cells, max_swamp_distance)
                propagate_swamp(i, j + 1, visited_cells, max_swamp_distance)
            elif is_near_water(i, j) and random.random() < swamp_threshold:
                terrain_grid[i, j] = 4  # Swamp
            elif terrain_heights[i, j] < 55:
                terrain_grid[i, j] = 0  # Open space
            elif terrain_heights[i, j] < 80:
                terrain_grid[i, j] = 1  # Forest
            elif terrain_heights[i, j] < 95:
                terrain_grid[i, j] = 3  # Mountain
            else:
                terrain_grid[i, j] = 5  # Lava

    # Additional pass to fill gaps and smooth out swamps
    for i in range(grid_size[0]):
        for j in range (grid_size[1]):
            if terrain_grid[i, j] == 4:
                # Expand swamps to adjacent open spaces to fill gaps
                neighbors = [
                    (i - 1, j),
                    (i + 1, j),
                    (i, j - 1),
                    (i, j + 1),
                ]
                for nx, ny in neighbors:
                    if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1] and terrain_grid[nx][ny] == 0:
                        if random.random() < swamp_threshold:
                            terrain_grid[nx][ny] = 4  # Convert open space to swamp

    return terrain_grid, terrain_heights

# Use the terrain grid instead of the random grid
grid_size = (300, 300)

# Start and goal positions
start = (10, 10)
goal = (250, 220)

grid, terrain_heights = create_terrain_grid(grid_size, start)

# Find paths with different algorithms
astar_path = astar(grid, start, goal)
dijkstra_path = dijkstra(grid, start, goal)

# Calculate path times
astar_time = calculate_path_time(astar_path, grid, terrain_heights)
dijkstra_time = calculate_path_time(dijkstra_path, grid, terrain_heights)

print(f"A* algorithm time: {astar_time:.2f} hours")
print(f"Dijkstra's algorithm time: {dijkstra_time:.2f} hours")

# Create the list of paths
paths = [astar_path, dijkstra_path]

# Visualize each path in its own subplot
visualize_paths(grid, start, goal, paths)

# Visualize the terrain heightmap
plt.figure(figsize=(12, 6))
plt.imshow(terrain_heights, cmap='terrain')
plt.colorbar(label='Height (m)')
plt.title('Terrain Heightmap')
plt.show()