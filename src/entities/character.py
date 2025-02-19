from settings import *
from entities.sprite import Sprite
from pygame.sprite import spritecollide
from abc import ABC, abstractmethod


class Character(ABC, Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, platform_group, delta_time):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(delta_time, platform_group)
        self.detect_platform_contact(platform_group)

    def input(self):
        pass

    @abstractmethod
    def move(self, delta_time):
        pass

    @abstractmethod
    def detect_platform_contact(self, platform_group):
        pass
