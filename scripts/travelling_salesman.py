import random
import math
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, cities, population_size=100, mutation_rate=0.01):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            # Create a random chromosome
            chromosome = list(self.cities.keys())
            random.shuffle(chromosome)
            population.append(chromosome)
        return population

    def fitness(self, chromosome):
        # Calculate the fitness of a chromosome (the total distance)
        distance = 0
        for i in range(len(chromosome)):
            city1 = self.cities[chromosome[i]]
            city2 = self.cities[chromosome[(i+1) % len(chromosome)]]
            distance += math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
        return -distance

    def selection(self, population):
        # Perform selection by choosing the top 20% of the population
        population.sort(key=lambda c: self.fitness(c), reverse=True)
        selected = population[:int(len(population) * 0.2)]
        return selected

    def crossover(self, selected):
        # Perform crossover by randomly selecting a pair of parents
        # and swapping their halves to produce two new offspring
        offspring = []
        for i in range(len(selected)):
            parent1 = selected[i]
            parent2 = selected[(i+1) % len(selected)]
            pivot = len(selected) // 2
            offspring1 = parent1[:pivot] + parent2[pivot:]
            offspring2 = parent2[:pivot] + parent1[pivot:]
            offspring.append(offspring1)
            offspring.append(offspring2)
        return offspring

    def mutation(self, offspring):
        # Perform mutation by randomly swapping two cities in 1% of the chromosomes
        for chromosome in offspring:
            if random.random() < self.mutation_rate:
                idx1, idx2 = random.sample(range(len(chromosome)), 2)
                chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return offspring

    def run(self, num_generations):
        population = self.initialize_population()
        for _ in range(num_generations):
            selected = self.selection(population)
            offspring = self.crossover(selected)
            population = self.mutation(offspring)
            if not population:
                # If the population becomes empty, reinitialize it
                population = self.initialize_population()
        return population

# Create a list of cities
cities = {
    'A': (1, 1),
    'B': (2, 3),
    'C': (5, 4),
    'D': (7, 3),
    'E': (5, 7),
    'F': (4, 5),
    'G': (2, 8),
    'H': (1, 6),
}

# Initialize the genetic algorithm
ga = GeneticAlgorithm(cities)

# Run the genetic algorithm for 100 generations
population = ga.run(100)

# Print the best chromosome
best_chromosome = max(population, key=ga.fitness)
print('Best Chromosome:', best_chromosome)
print('Fitness:', -ga.fitness(best_chromosome))  # Absolute value for positive distance

# Plot the cities and the best chromosome
plt.figure(figsize=(8, 8))
for city in cities.keys():
    plt.scatter(*cities[city])
    plt.text(*cities[city], city)
for i in range(len(best_chromosome)):
    city1 = cities[best_chromosome[i]]
    city2 = cities[best_chromosome[(i+1) % len(best_chromosome)]]
    plt.plot([city1[0], city2[0]], [city1[1], city2[1]], c='r')
plt.show()