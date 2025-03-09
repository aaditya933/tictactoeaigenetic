import numpy as np
import random
import pygame
import os
import matplotlib.pyplot as plt

# Pygame settings
WIDTH, HEIGHT = 300, 300
SQUARE_SIZE = WIDTH // 3
LINE_WIDTH = 5
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Tic Tac Toe AI Training")

class GeneticAI:
    def __init__(self, population_size=90, mutation_rate=0.1, generations=500):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = [self.create_random_strategy() for _ in range(population_size)]

    def create_random_strategy(self):
        return np.random.rand(3, 3) * 2 - 1  # Values range from -1 to 1

    def evaluate(self, strategy):
        """Improved fitness function for AI"""
        score = 0
        for _ in range(10):  # Simulate 10 games per strategy
            board = [[None] * 3 for _ in range(3)]
            result = self.simulate_game(strategy, board)
            if result == "win":
                score += 10
            elif result == "draw":
                score += 2
            elif result == "loss":
                score -= 5
        return score

    def simulate_game(self, strategy, board):
        """Visualize AI playing Tic-Tac-Toe"""
        # screen.fill(WHITE)
        # draw_grid()

        for _ in range(9):
            move = self.select_best_move(strategy, board)
            if move is None:
                break
            row, col = move
            board[row][col] = 'X'
            # draw_board(board)
            # pygame.display.update()
            # pygame.time.delay(500)

            if self.check_winner(board, 'X'):
                return "win"

            self.smart_opponent_move(board)  # Dynamic opponent
            # draw_board(board)
            # pygame.display.update()
            # pygame.time.delay(500)

            if self.check_winner(board, 'O'):
                return "loss"

        return "draw"

    def select_best_move(self, strategy, board):
        """Select the best move based on strategy values."""
        best_score = -float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    if strategy[row][col] > best_score:
                        best_score = strategy[row][col]
                        best_move = (row, col)
        return best_move

    def smart_opponent_move(self, board):
        """Opponent tries to block AI from winning."""
        empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]

        # Try to win
        for row, col in empty_positions:
            board[row][col] = 'O'
            if self.check_winner(board, 'O'):
                return
            board[row][col] = None  # Undo

        # Try to block AI from winning
        for row, col in empty_positions:
            board[row][col] = 'X'
            if self.check_winner(board, 'X'):
                board[row][col] = 'O'
                return
            board[row][col] = None  # Undo

        # If no immediate threat, play randomly
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
            mutation = np.random.normal(0, 0.3, (3, 3))  # Stronger mutation
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
        self.population = [x[1] for x in scores[:self.population_size // 2]]
        while len(self.population) < self.population_size:
            parent1, parent2 = random.sample(self.population, 2)
            self.population.append(self.crossover(parent1, parent2))

    def get_best_strategy(self):
        return max(self.population, key=self.evaluate)

    def visualize_learning(self):
        """Train AI and save the best strategy."""
        fitness_progress = []

        for generation in range(self.generations):
            self.evolve()
            best_strategy = self.get_best_strategy()
            best_fitness = self.evaluate(best_strategy)
            fitness_progress.append(best_fitness)
            
            print(f"Generation {generation + 1}/{self.generations} - Best Fitness: {best_fitness}")

            board = [[None] * 3 for _ in range(3)]
            self.simulate_game(best_strategy, board)

        np.save("best_strategy.npy", best_strategy)
        print("Training complete! Best strategy saved as best_strategy.npy")

        plt.plot(fitness_progress)
        plt.xlabel("Generations")
        plt.ylabel("Best Fitness Score")
        plt.title("Genetic Algorithm Training Progress")
        plt.savefig("training_progress.png")
        plt.close()

# Pygame visualization functions
# def draw_grid():
#     """Draws the Tic-Tac-Toe grid."""
#     for i in range(1, 3):
#         pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
#         pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# def draw_board(board):
#     """Draws the board with Xs and Os."""
#     screen.fill(WHITE)
#     draw_grid()
#     for row in range(3):
#         for col in range(3):
#             if board[row][col] == "X":
#                 pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20),
#                                  (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), LINE_WIDTH)
#                 pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20),
#                                  (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), LINE_WIDTH)
#             elif board[row][col] == "O":
#                 pygame.draw.circle(screen, RED, 
#                                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
#                                    SQUARE_SIZE // 3, LINE_WIDTH)
#     pygame.display.update()

# Run training and visualization
if __name__ == "__main__":
    ai = GeneticAI()
    ai.visualize_learning()
    pygame.quit()
