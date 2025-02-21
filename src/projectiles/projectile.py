from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, delta_time, speed, groups):
        super().__init__(pos, surf, groups)
        self.delta_time = delta_time
        self.direction = direction
        self.speed = speed

    def update(self):
        self.old_rect = self.rect.copy()
        self._move(self.delta_time)
        self._check_out_of_bounds()

    @abstractmethod
    def _move(self, delta_time):
        pass

    def _check_out_of_bounds(self):
        boundary = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        if not self.rect.colliderect(boundary):
            self.kill()
