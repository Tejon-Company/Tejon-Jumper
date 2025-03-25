import pygame
import sys
from pygame.math import Vector2 as vector
from enum import Enum, auto
from os.path import join


class Difficulty(Enum):
    EASY = auto()
    HARD = auto()


class GameConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.difficulty = Difficulty.EASY
        self.window_width = 1280
        self.window_height = 720
        self.tile_size = 32
        self.animation_speed = 6
        self.parallax_factor = [0.1, 0.2, 0.4, 0.9]

    def set_difficulty(self, difficulty: Difficulty):
        self.difficulty = difficulty

    def get_resolution(self):
        return self.window_width, self.window_height


config = GameConfig()

