"""
This file contains all the settings/constants for the game.
"""

# Sizes
GRID_SIZE = 16
WIDTH, HEIGHT = GRID_SIZE * 60, (GRID_SIZE - 4) * 60
CELL_SIZE = WIDTH // GRID_SIZE  # Calculate new cell size

# Colors
ALLY_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)
INFO_AREA_HEIGHT = 90
INFO_BG_COLOR = (230, 230, 230)

# Bools
PLACING_PIECES = 0
GAME_STARTED = 1