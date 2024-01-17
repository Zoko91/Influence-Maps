"""
Calculate the influence of each cell on the grid and display it on the screen.
"""

from settings import *
import pygame


def draw_influence(screen, influence_image, influence_map, grid, village_image):
    # Constants
    margin = 5
    title_size = 36
    text_size = 22
    image_width, image_height = 40, 40
    village_text_color = (33, 33, 33)  # Orange
    title_text_color = (0, 0, 0)

    # Calculate the best village position based on the highest influence
    best_village_position = (0, 0)
    max_influence = -1  # Initialize
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Check if this cell has the highest influence
            if influence_map[x][y] > max_influence and grid[x][y] != "mountain" and grid[x][y] != "ally" and grid[x][y] != "enemy":
                max_influence = influence_map[x][y]
                best_village_position = (x, y)

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

    # Calculate the position of the village image
    village_image_x = best_village_position[0] * CELL_SIZE  # Adjust for grid position
    village_image_y = best_village_position[1] * CELL_SIZE  # Adjust for grid position

    # Display the village image at the calculated position
    screen.blit(village_image, (village_image_x, village_image_y))

    text_x_village = image_x + image_width + margin
    text_y_village = image_y + (image_height - text_surface_village.get_height()) // 2
    screen.blit(text_surface_village, (text_x_village, text_y_village))
    screen.blit(text_surface_location, (text_x_village+100, text_y_village+22))

    # Border
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT, WIDTH, INFO_AREA_HEIGHT), 1)


def calculate_influence(grid):
    influence_map = [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def add_influence(source_x, source_y, strength, decay_factor, max_distance):
        for x in range(max(0, source_x - max_distance),
                       min(GRID_SIZE, source_x + max_distance + 1)):
            for y in range(max(0, source_y - max_distance),
                           min(GRID_SIZE, source_y + max_distance + 1)):
                distance = abs(source_x - x) + abs(source_y - y)
                if distance <= max_distance:
                    influence = strength * ((max_distance - distance) * decay_factor)
                    influence_map[x][y] += influence

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == "ally":
                add_influence(x, y, ALLY_INFLUENCE_STRENGTH, ALLY_DECAY_FACTOR, ALLY_MAX_INFLUENCE_DISTANCE)
            elif grid[x][y] == "enemy":
                add_influence(x, y, ENEMY_INFLUENCE_STRENGTH, ENEMY_DECAY_FACTOR, ENEMY_MAX_INFLUENCE_DISTANCE)

    return influence_map

