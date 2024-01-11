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
from events import initialize_game

screen, font = initialize_game()

# Game state
game_state = PLACING_PIECES

# Grid state
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Load the images
wolf_image = pygame.image.load("../images/wolf.png")
water_image = pygame.image.load("../images/water.png")
mountain_image = pygame.image.load("../images/mountain.png")

# Resize the images to fit the cell size if needed
wolf_image = pygame.transform.scale(wolf_image, (CELL_SIZE, CELL_SIZE))
water_image = pygame.transform.scale(water_image, (CELL_SIZE, CELL_SIZE))
mountain_image = pygame.transform.scale(mountain_image, (CELL_SIZE, CELL_SIZE))


def main():
    from draw import draw_grid, draw_pieces, draw_legend, place_random_mountains
    from influence import draw_influence, calculate_influence

    global game_state
    running = True
    influence_map = None  # Initialize influence map

    place_random_mountains(grid)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == PLACING_PIECES and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if grid_y < GRID_SIZE:
                    if not grid[grid_x][grid_y] == "mountain":
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
            draw_pieces(grid, screen, wolf_image, water_image, mountain_image)
            # draw_legend(screen)
        elif game_state == GAME_STARTED:
            draw_grid(screen, influence_map)
            draw_pieces(grid, screen, wolf_image, water_image, mountain_image)
            draw_influence(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
