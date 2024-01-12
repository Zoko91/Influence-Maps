"""
Functions used to display elements on the grid.
"""

from settings import *
import pygame
from main import font
import random


def draw_grid(screen, influence_map, grid):
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            color = (255, 255, 255)  # Default color for neutral
            # Change color based on the influence value
            if influence_map[grid_x][grid_y] > 0:
                color = (8, 107, 160)   # Light green for allies
            elif influence_map[grid_x][grid_y] < 0:
                color = (230, 30, 30)  # Light red for enemies
            if grid[grid_x][grid_y] == "mountain":
                color = (196, 164, 132) # Light brown for mountains

            # Draw the cell with the appropriate color
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Grid lines


def draw_pieces(grid, screen, wolf_image, water_image, mountain_image):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_x = x * CELL_SIZE
            cell_y = y * CELL_SIZE

            if grid[x][y] == "ally":
                # Draw wolf image for allies
                screen.blit(water_image, (cell_x, cell_y))
            elif grid[x][y] == "enemy":
                # Draw water image for enemies
                screen.blit(wolf_image, (cell_x, cell_y))
            elif grid[x][y] == "mountain":
                # Draw mountain image for mountains
                screen.blit(mountain_image, (cell_x, cell_y))


def draw_legend(screen):
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


def place_random_mountains(grid):
    num_mountains = random.randint(3, 6)  # Randomly choose the number of mountains
    for _ in range(num_mountains):
        while True:
            ########################
            # ATTENTION MONTAGNE !!!
            ########################
            x = random.randint(0, GRID_SIZE - 1)  # Random x-coordinate
            y = random.randint(0, GRID_SIZE - 4 - 1)  # Random y-coordinate
            if grid[x][y] is None:  # Check if the cell is empty
                grid[x][y] = "mountain"
                break