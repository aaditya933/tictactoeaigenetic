import numpy as np
import random
import matplotlib.pyplot as plt

class GeneticAI:
    def __init__(self, population_size=50, mutation_rate=0.1, generations=1000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = [self.create_random_strategy() for _ in range(population_size)]

    def create_random_strategy(self):
        return np.random.rand(3, 3)  # Random weights for moves

    def evaluate(self, strategy):
        """Simulate games and return a fitness score."""
        return np.sum(strategy)  # Simplified evaluation for now

    def mutate(self, strategy):
        """Apply mutations to strategy."""
        if random.random() < self.mutation_rate:
            mutation = np.random.normal(0, 0.1, (3, 3))
            strategy += mutation
        return strategy

    def crossover(self, parent1, parent2):
        """Combine two strategies to create a new one."""
        child = (parent1 + parent2) / 2
        return self.mutate(child)

    def evolve(self):
        """Train AI using Genetic Algorithm."""
        for _ in range(self.generations):
            scores = [(self.evaluate(strategy), strategy) for strategy in self.population]
            scores.sort(reverse=True, key=lambda x: x[0])
            self.population = [x[1] for x in scores[:self.population_size // 2]]  # Keep top half
            while len(self.population) < self.population_size:
                parent1, parent2 = random.sample(self.population, 2)
                self.population.append(self.crossover(parent1, parent2))

    def get_best_strategy(self):
        return max(self.population, key=self.evaluate)

    def visualize_learning(self):
        """Visualize fitness progression over generations."""
        fitness_progress = []
        for _ in range(self.generations):
            self.evolve()
            best_fitness = self.evaluate(self.get_best_strategy())
            fitness_progress.append(best_fitness)
        plt.plot(fitness_progress)
        plt.xlabel("Generations")
        plt.ylabel("Best Fitness Score")
        plt.title("Genetic Algorithm Training Progress")
        plt.show()

if __name__ == "__main__":
    ai = GeneticAI()
    ai.visualize_learning()
