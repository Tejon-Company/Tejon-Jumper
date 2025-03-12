from settings import *
from characters.sprite import Sprite
from abc import ABC, abstractmethod
from resource_manager import ResourceManager


class Character(ABC, Sprite):
    def __init__(self, pos, surf, groups, platform_rects, sprite_sheet_name):
        super().__init__(pos, surf, groups)

        self.platform_rects = platform_rects

        self.sprite_sheet = ResourceManager.load_sprite_sheet(
            sprite_sheet_name)

    @abstractmethod
    def update(self, delta_time):
        pass
