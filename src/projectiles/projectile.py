from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.speed = None
        self.is_activated = False

    def update(self, platform_rects, delta_time):
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        self._reset_projectile_if_off_screen()

    def change_position(self, new_pos_x, new_pos_y):
        self.rect.x = new_pos_x
        self.rect.y = new_pos_y

    @abstractmethod
    def _move(self, delta_time):
        pass

    @abstractmethod
    def _reset_projectile_if_off_screen(self):
        pass
