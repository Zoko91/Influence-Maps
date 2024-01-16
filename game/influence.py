"""
Calculate the influence of each cell on the grid and display it on the screen.
"""

from settings import *
import pygame


def draw_influence(screen, influence_image, best_village_position=(0, 0)):
    # Constants
    margin = 5
    title_size = 36
    text_size = 22
    image_width, image_height = 40, 40
    village_text_color = (255, 128, 0)  # Orange
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
    village_text = 'The village has (finally) found a place to live !'
    village_location = f'X: {best_village_position[0]}     Y: {best_village_position[1]}'
    text_surface_village = font_main.render(village_text, True, village_text_color)
    text_surface_location = font_main.render(village_location, True, (255, 51, 51))  # Red

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
    screen.blit(text_surface_location, (text_x_village+100, text_y_village+22))

    # Border
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT), 1)


def calculate_influence(grid):
    ally_influence_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    enemy_influence_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def add_influence(source_x, source_y, ally_strength, enemy_strength, ally_decay_factor, enemy_decay_factor, ally_max_distance, enemy_max_distance):
        for x in range(max(0, source_x - ally_max_distance),
                       min(GRID_SIZE, source_x + ally_max_distance + 1)):
            for y in range(max(0, source_y - ally_max_distance),
                           min(GRID_SIZE, source_y + ally_max_distance + 1)):
                distance = abs(source_x - x) + abs(source_y - y)
                if distance <= ally_max_distance:
                    ally_influence = ally_strength * ((ally_max_distance - distance) * ally_decay_factor)
                    ally_influence_map[x][y] += ally_influence

        for x in range(max(0, source_x - enemy_max_distance),
                       min(GRID_SIZE, source_x + enemy_max_distance + 1)):
            for y in range(max(0, source_y - enemy_max_distance),
                           min(GRID_SIZE, source_y + enemy_max_distance + 1)):
                distance = abs(source_x - x) + abs(source_y - y)
                if distance <= enemy_max_distance:
                    enemy_influence = enemy_strength * ((enemy_max_distance - distance) * enemy_decay_factor)
                    enemy_influence_map[x][y] += enemy_influence

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == "ally":
                add_influence(x, y, ALLY_INFLUENCE_STRENGTH, 0.0, ALLY_DECAY_FACTOR, ENEMY_DECAY_FACTOR, ALLY_MAX_INFLUENCE_DISTANCE, ENEMY_MAX_INFLUENCE_DISTANCE)
            elif grid[x][y] == "enemy":
                add_influence(x, y, 0.0, ENEMY_INFLUENCE_STRENGTH, ALLY_DECAY_FACTOR, ENEMY_DECAY_FACTOR, ALLY_MAX_INFLUENCE_DISTANCE, ENEMY_MAX_INFLUENCE_DISTANCE)

    return ally_influence_map, enemy_influence_map


