import random
import matplotlib.pyplot as plt

# Define cities with their (x, y) coordinates
cities = {
    'A': (1, 1), 'B': (2, 3), 'C': (5, 4), 'D': (7, 3),
    'E': (5, 7), 'F': (4, 5), 'G': (2, 8), 'H': (1, 6),
}

def calculate_distance(route):
    """Calculate the total distance for a given route."""
    distance = 0
    for i in range(len(route) - 1):
        city1 = cities[route[i]]
        city2 = cities[route[i + 1]]
        distance += ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5
    # Add distance to return to the starting city
    city1 = cities[route[-1]]
    city2 = cities[route[0]]
    distance += ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5
    return distance

def create_initial_population(size):
    """Create an initial population of random routes."""
    population = []
    for _ in range(size):
        route = list(cities.keys())
        random.shuffle(route)
        population.append(route)
    return population

def order_crossover(parent1, parent2):
    """Perform Order Crossover (OX) between two parents."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    # Get a slice from parent1
    child = [None] * size
    child[start:end] = parent1[start:end]

    # Fill in the remaining cities from parent2
    fill_pos = end
    for city in parent2:
        if city not in child:
            if fill_pos == size:
                fill_pos = 0
            child[fill_pos] = city
            fill_pos += 1
    return child

def mutation(route, mutation_rate):
    """Perform mutation using inversion mutation."""
    if random.random() < mutation_rate:
        idx1, idx2 = sorted(random.sample(range(len(route)), 2))
        route[idx1:idx2] = reversed(route[idx1:idx2])
    return route

def genetic_algorithm(population_size=100, generations=500, mutation_rate=0.01, elitism=True):
    """Run the genetic algorithm."""
    population = create_initial_population(population_size)

    for _ in range(generations):
        # Sort population by fitness (distance)
        population = sorted(population, key=lambda x: calculate_distance(x))

        # Elitism: Preserve the best solution
        new_population = [population[0]] if elitism else []

        # Select top 20% for breeding
        selection_size = max(2, population_size // 5)
        selected = population[:selection_size]

        # Create new population using crossover
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = order_crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_population.append(child)

        population = new_population

    # Return the best route found
    best_route = min(population, key=lambda x: calculate_distance(x))
    return best_route, calculate_distance(best_route)

# Run the genetic algorithm and get the best route and distance
best_route, best_distance = genetic_algorithm()
print(f"Best route: {best_route}")
print(f"Best distance: {best_distance:.2f}")

# Plot the best route
x = [cities[city][0] for city in best_route]
y = [cities[city][1] for city in best_route]

# Close the loop by appending the start point to the end
x.append(x[0])
y.append(y[0])

plt.figure(figsize=(8, 8))
plt.plot(x, y, '-o', label='Route')
for city, coords in cities.items():
    plt.text(coords[0], coords[1], city, fontsize=12)
plt.title('Best Route Found by Genetic Algorithm')
plt.xlabel('X Coordinates')
plt.ylabel('Y Coordinates')
plt.legend()
plt.grid(True)
plt.show()
