import pygame
import sys
from pygame.math import Vector2 as vector
from enum import Enum, auto


class Difficulty(Enum):
    NORMAL = auto()
    HIGH = auto()


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

TILE_SIZE = 32
ANIMATION_SPEED = 6

DIFFICULTY = Difficulty.NORMAL
