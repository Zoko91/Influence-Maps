from settings import *
import pygame


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_AREA_HEIGHT))
    font = pygame.font.Font(None, 30)
    return screen, font