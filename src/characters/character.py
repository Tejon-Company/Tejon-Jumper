from settings import *
from characters.sprite import Sprite
from abc import ABC, abstractmethod
from resource_manager import ResourceManager


class Character(ABC, Sprite):
    def __init__(self, pos, surf, groups, platform_rects):
        super().__init__(pos, surf, groups)

        self.platform_rects = platform_rects

    @abstractmethod
    def update(self, delta_time):
        pass
