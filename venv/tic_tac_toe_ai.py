import numpy as np
import random
import matplotlib.pyplot as plt

class GeneticAI:
    def __init__(self, population_size=100, mutation_rate=0.1, generations=1000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = [self.create_random_strategy() for _ in range(population_size)]

    def create_random_strategy(self):
        return np.random.rand(3, 3)  # Random weights for moves

    def evaluate(self, strategy):
        score = 0
        for _ in range(10):  # Simulate 10 games per strategy
            board = [[None] * 3 for _ in range(3)]
            result = self.simulate_game(strategy, board)
            if result == "win":
                score += 3
            elif result == "draw":
                score += 1
            elif result == "loss":
                score -= 1
        return score

    def simulate_game(self, strategy, board):
           for _ in range(9):
               move = self.select_best_move(strategy, board)
               if move is None:
                   break
               row, col = move
               board[row][col] = 'X'
               # draw_board(board)
               # pygame.display.update()
               # pygame.time.delay(500)  # Show move for better visualization
   
               if self.check_winner(board, 'X'):
                   return "win"
   
               self.random_opponent_move(board)
            # draw_board(board)
               # pygame.display.update()
            # pygame.time.delay(500)

               if self.check_winner(board, 'O'):
                   return "loss"
           return "draw"


    def select_best_move(self, strategy, board):
        """Select the best move based on strategy values."""
        best_score = -1
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    if strategy[row][col] > best_score:
                        best_score = strategy[row][col]
                        best_move = (row, col)
        return best_move

    def random_opponent_move(self, board):
        """Make a random move for the opponent."""
        empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
        if empty_positions:
            row, col = random.choice(empty_positions)
            board[row][col] = 'O'

    def check_winner(self, board, player):
        """Check if a player has won."""
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

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
            best_strategy = self.get_best_strategy()
            best_fitness = self.evaluate(self.get_best_strategy())
            fitness_progress.append(best_fitness)

       
        np.save("best_strategy.npy", best_strategy)
        print("Training complete! Best strategy saved as best_strategy.npy")

    # Plot training progress
        plt.plot(fitness_progress)
        plt.xlabel("Generations")
        plt.ylabel("Best Fitness Score")
        plt.title("Genetic Algorithm Training Progress")
        plt.savefig("training_progress.png")  # Save plot instead of showing it
        plt.close()




    def get_ai_move(self, board):
        """Return the AI's best move for the current board state."""
        best_strategy = self.get_best_strategy()
        return self.select_best_move(best_strategy, board)

if __name__ == "__main__":
    ai = GeneticAI()
    ai.visualize_learning()
