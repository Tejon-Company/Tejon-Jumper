import pygame
import sys
from pygame.math import Vector2 as vector
from enum import Enum, auto
from os.path import join


class Difficulty(Enum):
    NORMAL = auto()
    HIGH = auto()


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

TILE_SIZE = 32
ANIMATION_SPEED = 6

PARALLAX_FACTOR = [0.1, 0.2, 0.4, 0.9]

DIFFICULTY = Difficulty.NORMAL

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)