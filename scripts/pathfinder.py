import numpy as np
import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

OBSTACLE_COST = 1e9
INFINITY = 1e9

def generate_grid(size, obstacle_probability=0.2, max_cost=10):
    grid = np.random.randint(1, max_cost, size=(size, size))
    grid[np.random.random(grid.shape) < obstacle_probability] = OBSTACLE_COST
    return grid

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def pathfinder(grid, start, end, heuristic_func=None):
    size = grid.shape[0]
    dist = np.full_like(grid, INFINITY, dtype=float)
    dist[start] = 0
    pq = [(0, start)]
    visited = set()
    parent = {}

    while pq:
        current_priority, current = heapq.heappop(pq)

        if current == end:
            break

        if current in visited:
            continue

        visited.add(current)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size and neighbor not in visited:
                if grid[neighbor] == OBSTACLE_COST:
                    continue

                new_cost = dist[current] + grid[neighbor]

                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    parent[neighbor] = current

                    if heuristic_func:
                        priority = new_cost + heuristic_func(neighbor, end)
                    else:
                        priority = new_cost

                    if neighbor not in visited:
                        heapq.heappush(pq, (priority, neighbor))

        yield visited, parent

    return dist, parent, visited

def dijkstra(grid, start, end):
    return pathfinder(grid, start, end)

def a_star(grid, start, end, heuristic='manhattan'):
    heuristic_func = manhattan_distance if heuristic == 'manhattan' else euclidean_distance
    return pathfinder(grid, start, end, heuristic_func)

def reconstruct_path(parent, end):
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    return path[::-1]

def visualize_animated(grid, start, end, dijkstra_generator, a_star_generator):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].set_title("Dijkstra's Algorithm")
    ax[1].set_title("A* Algorithm")

    for a in ax:
        a.imshow(grid, cmap='gray')
        a.scatter(start[1], start[0], color='green', label='Start')
        a.scatter(end[1], end[0], color='red', label='End')

    dijkstra_scatter = ax[0].scatter([], [], color='blue', alpha=0.5)
    a_star_scatter = ax[1].scatter([], [], color='blue', alpha=0.5)

    dijkstra_path_scatter = ax[0].scatter([], [], color='yellow', s=50)
    a_star_path_scatter = ax[1].scatter([], [], color='yellow', s=50)

    dijkstra_complete = False
    a_star_complete = False

    def update(frame):
        nonlocal dijkstra_complete, a_star_complete

        if not dijkstra_complete:
            try:
                for _ in range(10):
                    dijkstra_visited, dijkstra_parent = next(dijkstra_generator)
            except StopIteration:
                dijkstra_complete = True
                dijkstra_path = reconstruct_path(dijkstra_parent, end)
                dijkstra_path_scatter.set_offsets(np.array(dijkstra_path)[:, ::-1])
            else:
                dijkstra_scatter.set_offsets(np.array(list(dijkstra_visited))[:, ::-1])

        if not a_star_complete:
            try:
                for _ in range(10):
                    a_star_visited, a_star_parent = next(a_star_generator)
            except StopIteration:
                a_star_complete = True
                a_star_path = reconstruct_path(a_star_parent, end)
                a_star_path_scatter.set_offsets(np.array(a_star_path)[:, ::-1])
            else:
                a_star_scatter.set_offsets(np.array(list(a_star_visited))[:, ::-1])

        if dijkstra_complete and a_star_complete:
            ani.event_source.stop()

        return dijkstra_scatter, a_star_scatter, dijkstra_path_scatter, a_star_path_scatter

    ani = animation.FuncAnimation(fig, update, frames=None, interval=300, blit=True, repeat=False, cache_frame_data=False)
    plt.show()

def compare_algorithms(size=20):
    grid = generate_grid(size)
    start = (0, 0)
    end = (size - 1, size - 1)

    start_time = time.time()
    dijkstra_generator = dijkstra(grid, start, end)
    dijkstra_gen_copy = dijkstra(grid, start, end)
    for visited, parent in dijkstra_gen_copy:
        pass
    dijkstra_time = time.time() - start_time
    dijkstra_visited_count = len(visited)

    start_time = time.time()
    a_star_generator = a_star(grid, start, end)
    a_star_gen_copy = a_star(grid, start, end)
    for visited, parent in a_star_gen_copy:
        pass
    a_star_time = time.time() - start_time
    a_star_visited_count = len(visited)

    print(f"Dijkstra's Algorithm: Visited {dijkstra_visited_count} nodes in {dijkstra_time:.4f} seconds.")
    print(f"A* Algorithm: Visited {a_star_visited_count} nodes in {a_star_time:.4f} seconds.")

    visualize_animated(grid, start, end, dijkstra_generator, a_star_generator)

compare_algorithms()
