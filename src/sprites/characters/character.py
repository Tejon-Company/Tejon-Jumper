from abc import ABC, abstractmethod

from sprites.sprite import Sprite
from singletons.settings.resolution_settings import ResolutionSettings


class Character(ABC, Sprite):
    def __init__(self, pos, surf, groups, platform_rects):
        super().__init__(pos, surf, groups)

        self.resolution_settings = ResolutionSettings()

        self._ratio = self.resolution_settings.tile_size / 64

        self.platform_rects = platform_rects

    @abstractmethod
    def update(self, delta_time):
        pass
