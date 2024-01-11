"""
Projet pour le cours : "IA pour les jeux vidéos"
Auteur : Joseph Beasse
Enseirb-Matmeca 2024

Objectif : Créer une carte de jeu pour y inférer une map d'influence selon les élements placés.
"""

# Imports
import pygame
import sys
from settings import *

# Initialisation
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_AREA_HEIGHT))
font = pygame.font.Font(None, 30)

# Game state
game_state = PLACING_PIECES

# Grid state
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def main():
    from draw import draw_grid, draw_pieces, draw_legend
    from influence import draw_influence, calculate_influence

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
                    influence_map = calculate_influence(grid)

        screen.fill((0, 0, 0))

        if game_state == PLACING_PIECES:
            draw_grid(screen, [[0]*GRID_SIZE for _ in range(GRID_SIZE)])
            draw_pieces(grid, screen)
            draw_legend(screen)
        elif game_state == GAME_STARTED:
            draw_grid(screen, influence_map)
            draw_pieces(grid, screen)
            draw_influence(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
