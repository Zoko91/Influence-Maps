"""
Projet pour le cours : "IA pour les jeux vidéos"
Auteur : Joseph Beasse
Enseirb-Matmeca 2024

Objectif : Créer une carte de jeu pour y inférer une map d'influence selon les élements placés.
"""

# Imports
import pygame
import sys

# Initialisation
pygame.init()

# Constants
GRID_SIZE = 9
WIDTH, HEIGHT = GRID_SIZE*100, (GRID_SIZE-2)*100

CELL_SIZE = WIDTH // GRID_SIZE
ALLY_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)
INFO_AREA_HEIGHT = 90
INFO_BG_COLOR = (230, 230, 230)

# Set up the display and font
screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_AREA_HEIGHT))
font = pygame.font.Font(None, 30)

# Game states
PLACING_PIECES = 0
GAME_STARTED = 1
game_state = PLACING_PIECES

# Grid state
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def draw_grid(influence_map):
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            color = (255, 255, 255)  # Default color for neutral

            # Change color based on the influence value
            if influence_map[grid_x][grid_y] > 0:
                color = (0, 255, 0)  # Light green for allies
            elif influence_map[grid_x][grid_y] < 0:
                color = (255, 0, 0)  # Light red for enemies

            # Draw the cell with the appropriate color
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Grid lines


def draw_pieces():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == "ally":
                pygame.draw.circle(screen, ALLY_COLOR, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3)
            elif grid[x][y] == "enemy":
                pygame.draw.circle(screen, ENEMY_COLOR,
                                   (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


def draw_legend():
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT))

    # Instructions
    instructions = [
        'Left Click: Place Ally',
        'Right Click: Place Enemy',
        'Space: Draw Influence Map'
    ]

    # Height of the text to center it in the info area
    total_text_height = sum([font.size(text)[1] for text in instructions]) + (len(instructions) - 1) * 10
    start_y = HEIGHT + (INFO_AREA_HEIGHT - total_text_height) // 2

    for text in instructions:
        text_surface = font.render(text, True, FONT_COLOR)
        centered_x = (WIDTH - text_surface.get_width()) // 2
        screen.blit(text_surface, (centered_x, start_y))
        start_y += text_surface.get_height() + 10


def draw_influence():
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT))
    game_started_text = 'Drawing Influence Map'
    text_surface = font.render(game_started_text, True, (53, 40, 40))  # Red color
    centered_x = (WIDTH - text_surface.get_width()) // 2
    centered_y = HEIGHT + (INFO_AREA_HEIGHT - text_surface.get_height()) // 2
    screen.blit(text_surface, (centered_x, centered_y))


def calculate_influence():
    influence_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def add_influence(x, y, amount):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            influence_map[x][y] += amount

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == "ally":
                add_influence(x, y, 1)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            add_influence(x + dx, y + dy, 0.5)
            elif grid[x][y] == "enemy":
                add_influence(x, y, -1)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            add_influence(x + dx, y + dy, -0.5)

    return influence_map


def main():
    global game_state
    running = True
    influence_map = None  # Initialize influence map

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == PLACING_PIECES and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if grid_y < GRID_SIZE:
                    if event.button == 1:
                        grid[grid_x][grid_y] = "ally"
                    elif event.button == 3:
                        grid[grid_x][grid_y] = "enemy"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state != GAME_STARTED:
                    game_state = GAME_STARTED
                    influence_map = calculate_influence()

        screen.fill((0, 0, 0))

        if game_state == PLACING_PIECES:
            draw_grid([[0]*GRID_SIZE for _ in range(GRID_SIZE)])
            draw_pieces()
            draw_legend()
        elif game_state == GAME_STARTED:
            draw_grid(influence_map)
            draw_pieces()
            draw_influence()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
