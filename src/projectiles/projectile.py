from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite
from resource_manager import ResourceManager


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.speed = None
        self.is_activated = False
        self.sprite_sheet = ResourceManager.load_sprite_sheet(
            sprite_sheet_name)
        self.animations = animations

    def update(self, delta_time):
        if not self.is_activated:
            return
        self._reset_projectile_if_off_screen()
        self._setup_animation()
        self.old_rect = self.rect.copy()
        self._move(delta_time)

    def _setup_animation(self):
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0

    @abstractmethod
    def change_position(self, new_pos_x, new_pos_y):
        pass

    @abstractmethod
    def _move(self, delta_time):
        pass

    @abstractmethod
    def _reset_projectile_if_off_screen(self):
        pass
