"""
Handle clicks, key presses, and other events.
Starts game loop and initializes the game.
"""
from settings import *
import pygame


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_AREA_HEIGHT))
    font = pygame.font.Font(None, 25)
    return screen, font


def handle_events(grid, game_state, influence_map):
    from influence import calculate_influence
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, None, game_state

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
            if event.key == pygame.K_ESCAPE:
                return False, None, game_state

    return True, influence_map, game_state
