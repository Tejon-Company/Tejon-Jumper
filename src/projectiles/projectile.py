from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, speed, groups):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.speed = speed

    def update(self, platform_rects, delta_time):
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        self._check_out_of_bounds()

    @abstractmethod
    def _move(self, delta_time):
        pass

    def _check_out_of_bounds(self):
        boundary = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        if not self.rect.colliderect(boundary):
            self.kill()
