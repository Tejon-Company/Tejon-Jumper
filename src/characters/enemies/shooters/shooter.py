from settings import *
from characters.enemies.enemy import Enemy
from projectiles.projectile import Projectile
from abc import ABC, abstractmethod


class Shooter(Enemy, ABC):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.shoot_cooldown = 2000
        self.last_shot = 0
        self.projectiles = pygame.sprite.Group()
        self.projectile = Projectile

    def update(self, platform_rects, delta_time):
        super().update(platform_rects, delta_time)
        self._shoot(delta_time)
        self.projectiles.update()

    @abstractmethod
    def _shoot(self, delta_time):
        pass
