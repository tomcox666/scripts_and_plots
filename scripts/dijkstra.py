import heapq

def dijkstra(graph, source, destination):
    """
    Finds the shortest path between two nodes in a weighted graph using Dijkstra's algorithm.

    Args:
        graph: A dictionary representing the graph, where keys are nodes and values are dictionaries of neighbors with their corresponding edge weights.
        source: The starting node.
        destination: The destination node.

    Returns:
        A tuple containing the shortest path distance and the path itself (as a list of nodes).
    """

    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == destination:
            break

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path = path[::-1]

    return distances[destination], path

# Example graph representation
graph = {
    'A': {'B': 2, 'C': 5, 'D': 1},
    'B': {'A': 2, 'C': 3, 'E': 1},
    'C': {'A': 5, 'B': 3, 'D': 2, 'F': 3},
    'D': {'A': 1, 'C': 2, 'F': 4},
    'E': {'B': 1, 'F': 6, 'G': 2},
    'F': {'C': 3, 'D': 4, 'E': 6, 'G': 1},
    'G': {'E': 2, 'F': 1}
}

# Find shortest path from 'A' to 'D'
shortest_distance, shortest_path = dijkstra(graph, 'A', 'G')

print("Shortest distance:", shortest_distance)
print("Shortest path:", shortest_path)