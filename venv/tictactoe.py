import pygame
import numpy as np
import os
from tic_tac_toe_ai import GeneticAI

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe with AI")
screen.fill(WHITE)

# Load AI
ai = GeneticAI()
if os.path.exists("best_strategy.npy"):
    ai_best_strategy = np.load("best_strategy.npy")
else:
    print("No trained AI found! Run tic_tac_toe_ai.py first.")
    exit()

# Board setup
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
player = "O"  # Human plays 'O', AI plays 'X'
game_over = False

# Draw grid lines
def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw marks (X or O)
def draw_marks():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + 30),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 30, row * SQUARE_SIZE + SQUARE_SIZE - 30), LINE_WIDTH)
                pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE - 30, row * SQUARE_SIZE + 30),
                                 (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + SQUARE_SIZE - 30), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, RED, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   SQUARE_SIZE // 3, LINE_WIDTH)

# Check winner
def check_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

# AI Move
def ai_move():
    global player
    best_move = ai.select_best_move(ai_best_strategy, board)
    if best_move:
        board[best_move[0]][best_move[1]] = "X"
        if check_winner("X"):
            print("AI Wins!")
            return True
    player = "O"  # Switch back to human
    return False

# Main loop
draw_grid()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == "O":
            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            if board[row][col] is None:
                board[row][col] = "O"
                if check_winner("O"):
                    print("You Win!")
                    game_over = True
                else:
                    game_over = ai_move()  # AI moves after you

    screen.fill(WHITE)
    draw_grid()
    draw_marks()
    pygame.display.update()

pygame.quit()
