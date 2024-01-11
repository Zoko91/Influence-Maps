"""
Functions used to display elements on the grid.
"""

from settings import *
import pygame
from main import font


def draw_grid(screen, influence_map):
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


def draw_pieces(grid, screen):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == "ally":
                pygame.draw.circle(screen, ALLY_COLOR, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3)
            elif grid[x][y] == "enemy":
                pygame.draw.circle(screen, ENEMY_COLOR,
                                   (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


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