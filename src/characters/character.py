from settings import *
from characters.sprite import Sprite
from pygame.sprite import spritecollide
from abc import ABC, abstractmethod


class Character(ABC, Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = surf

    @abstractmethod
    def update(self, platform_rects, delta_time):
        pass
