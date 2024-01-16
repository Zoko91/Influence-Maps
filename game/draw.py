"""
Contains function to draw elements on the screen like images, grid, text, etc.
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
                color = (196, 164, 132)  # Light brown for mountains

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


def draw_legend(screen, wolf_icon, ally_icon):
    margin = 5
    icon_size = 28
    title_size = 36
    padding_between_icons = 45
    neutral_text_color = FONT_COLOR
    legend_title_color = (0, 0, 0)

    # Clear legend area
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT))

    # Title // Legend
    title_font = pygame.font.Font(None, title_size)
    title_surface = title_font.render('Legend', True, legend_title_color)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT + margin))

    y_position = HEIGHT + title_surface.get_height() + margin
    legend_items = [
        {"description": 'Left Click: Place Ally', "icon": ally_icon, "color": (8, 107, 160)},
        {"description": 'Right Click: Place Enemy', "icon": wolf_icon, "color": (230, 30, 30)},
    ]

    # X position to center the icons and text horizontally
    total_width_of_legend_items = sum([font.size(item["description"])[0] + icon_size for item in legend_items])
    total_width_of_legend_items += padding_between_icons * (len(legend_items) - 1)
    start_x = (WIDTH - total_width_of_legend_items) // 2 + 15

    # Render
    for item in legend_items:
        if item["icon"]:
            icon = pygame.transform.scale(item["icon"], (icon_size, icon_size))
            screen.blit(icon, (start_x, y_position))

        text_surface = font.render(item["description"], True, item["color"])
        text_x = start_x + icon_size + margin
        screen.blit(text_surface, (text_x, y_position+8))

        # Resets start_x for next item
        start_x += font.size(item["description"])[0] + icon_size + padding_between_icons

    # Game control instructions
    controls_text = 'Space: Start Game   |   Escape: End Game'
    controls_surface = font.render(controls_text, True, neutral_text_color)
    controls_x = WIDTH // 2 - controls_surface.get_width() // 2
    y_position += icon_size + margin  # Update y_position for the control instructions
    screen.blit(controls_surface, (controls_x, y_position))
    # Borders
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT), 1)


def place_random_mountains(grid):
    num_mountains = random.randint(3, 6)
    for _ in range(num_mountains):
        while True:
            ########################
            # ATTENTION MOUNTAINS !!!
            ########################
            x = random.randint(0, GRID_SIZE - 1)  # Random x-coordinate
            y = random.randint(0, GRID_SIZE - 4 - 1)  # Random y-coordinate
            if grid[x][y] is None:
                grid[x][y] = "mountain"
                break
