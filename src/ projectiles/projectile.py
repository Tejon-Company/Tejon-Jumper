from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite


class Projectile(ABC, Sprite):
    def __init__(self, pos, surf, direction, speed, groups):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.speed = speed

    @abstractmethod
    def update(self, delta_time):
        pass
