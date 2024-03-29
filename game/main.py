"""
Projet of the course : "IA pour les jeux vidéos"
Author : Joseph Beasse
Enseirb-Matmeca 2024

Goal : Implement a game of "Wolf and Sheep" with an influence map.
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
legend_bg = pygame.image.load("../images/parchemin.png")
wolf_icon = pygame.image.load("../images/wolf_small.png")
ally_icon = pygame.image.load("../images/water_small.png")
influence_image = pygame.image.load("../images/firework2.png")
village_image = pygame.image.load("../images/village.png")

# Resize the images to fit the cell size if needed
wolf_image = pygame.transform.scale(wolf_image, (CELL_SIZE, CELL_SIZE))
water_image = pygame.transform.scale(water_image, (CELL_SIZE, CELL_SIZE))
mountain_image = pygame.transform.scale(mountain_image, (CELL_SIZE, CELL_SIZE))
village_image = pygame.transform.scale(village_image, (CELL_SIZE, CELL_SIZE))


def main():
    from draw import draw_grid, draw_pieces, draw_legend, place_random_mountains
    from influence import draw_influence
    from events import handle_events

    # Initialize the game
    global game_state
    running = True
    place_random_mountains(grid)
    influence_map = None

    while running:
        running, influence_map, game_state = handle_events(grid, game_state, influence_map)
        screen.fill((0, 0, 0))

        if game_state == PLACING_PIECES:
            draw_grid(screen, None, grid)
            draw_pieces(grid, screen, wolf_image, water_image, mountain_image)
            draw_legend(screen, wolf_icon, ally_icon)
        elif game_state == GAME_STARTED and influence_map is not None:
            draw_grid(screen, influence_map, grid)
            draw_pieces(grid, screen, wolf_image, water_image, mountain_image)
            draw_influence(screen, influence_image, influence_map, grid, village_image)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
