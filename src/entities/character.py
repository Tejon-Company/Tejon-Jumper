from settings import *
from entities.sprite import Sprite
from pygame.sprite import spritecollide
from abc import ABC, abstractmethod


class Character(ABC, Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, platform_rects, delta_time):
        self.old_rect = self.rect.copy()
        self._input()
        self._move(platform_rects, delta_time)
        self._detect_platform_contact(platform_rects)

    def _input(self):
        pass

    @abstractmethod
    def _move(self, platform_rects, delta_time):
        pass

    @abstractmethod
    def _detect_platform_contact(self, platform_rects):
        pass
