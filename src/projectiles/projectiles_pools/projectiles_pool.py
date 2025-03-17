from settings import *
from abc import ABC, abstractmethod
from typing import Optional


class ProjectilesPool(ABC):
    def __init__(self, size, projectile_groups, game):
        self.pool = list()
        self.size = size
        self.projectile_groups = projectile_groups
        self.game = game
        self._create_pool()

    @abstractmethod
    def _create_pool(self):
        pass

    @abstractmethod
    def shoot(self, pos_x, pos_y, direction: Optional[tuple] = None):
        pass

    def _create_animation_rects(self, frame_start_x, number_of_frames):
        frame_start_x *= 16
        sprite_size = 16
        y = 0
        pixel_gap = 1
        animation_rects = []

        for i in range(number_of_frames):
            x = (frame_start_x + frame_start_x//16) + \
                (sprite_size * i) + (i * pixel_gap)
            animation_rects.append((x, y, sprite_size, sprite_size))

        return animation_rects
