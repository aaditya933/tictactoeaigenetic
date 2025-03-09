import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)

# Fonts
FONT = pygame.font.Font(None, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
current_player = "X"
paused = False

# Draw grid
for row in range(1, BOARD_ROWS):
    pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
for col in range(1, BOARD_COLS):
    pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                start_pos1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_pos1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, WHITE, start_pos1, end_pos1, CROSS_WIDTH)
                start_pos2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_pos2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, WHITE, start_pos2, end_pos2, CROSS_WIDTH)

def check_winner():
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def display_winner(winner):
    screen.fill(BG_COLOR)
    text = FONT.render(f"Player {winner} wins!", True, RED)
    screen.blit(text, (WIDTH // 3, HEIGHT // 3))
    pygame.display.flip()
    pygame.time.delay(2000)

def restart_game():
    global board, current_player, paused
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    current_player = "X"
    paused = False
    screen.fill(BG_COLOR)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def toggle_pause():
    global paused
    paused = not paused

def main():
    global current_player
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not paused:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = current_player
                    winner = check_winner()
                    if winner:
                        display_winner(winner)
                        restart_game()
                    current_player = "O" if current_player == "X" else "X"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                if event.key == pygame.K_p:
                    toggle_pause()
        draw_figures()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
