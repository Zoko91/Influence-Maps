"""
Functions used to calculate and display the influence map
"""

from settings import *
import pygame


def draw_influence(screen, influence_image, best_village_position=(0, 0)):
    # Constants
    margin = 5
    title_size = 36
    text_size = 22
    image_width, image_height = 40, 40
    village_text_color = (255, 51, 51)  # Orange
    title_text_color = (0, 0, 0)

    # Clear the legend area
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT))

    # Title
    title_font = pygame.font.Font(None, title_size)
    title_surface = title_font.render('Game Ended', True, title_text_color)
    title_x = (WIDTH - title_surface.get_width()) // 2
    title_y = HEIGHT + margin
    screen.blit(title_surface, (title_x, title_y))

    # Image and font
    influence_image_scaled = pygame.transform.scale(influence_image, (image_width, image_height))
    font_main = pygame.font.Font(None, text_size)

    # Text
    village_text = f'The village has found a place to live (finally): {best_village_position[0]}, {best_village_position[1]}'
    text_surface_village = font_main.render(village_text, True, village_text_color)

    # Total width of the image and text to center them
    total_content_width = image_width + text_surface_village.get_width() + margin
    content_x_start = (WIDTH - total_content_width) // 2

    # Show the image and center horizontally with the text
    image_x = content_x_start
    image_y = title_y + title_surface.get_height() + margin
    screen.blit(influence_image_scaled, (image_x, image_y))

    text_x_village = image_x + image_width + margin
    text_y_village = image_y + (image_height - text_surface_village.get_height()) // 2
    screen.blit(text_surface_village, (text_x_village, text_y_village))

    # Border
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT), 1)


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
