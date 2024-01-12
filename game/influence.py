"""
Functions used to calculate and display the influence map
"""

from settings import *
import pygame
from main import font


def draw_influence(screen):
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT))
    game_started_text = 'Drawing Influence Map'
    text_surface = font.render(game_started_text, True, (53, 40, 40))  # Red color
    centered_x = (WIDTH - text_surface.get_width()) // 2
    centered_y = HEIGHT + (INFO_AREA_HEIGHT - text_surface.get_height()) // 2
    screen.blit(text_surface, (centered_x, centered_y))


def calculate_influence(grid):
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
