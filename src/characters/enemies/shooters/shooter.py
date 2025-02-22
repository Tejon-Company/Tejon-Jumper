from settings import *
from characters.enemies.enemy import Enemy
from abc import ABC, abstractmethod


class Shooter(Enemy, ABC):
    def __init__(self, pos, surf, groups, projectile_groups):
        super().__init__(pos, surf, groups)
        self.shoot_cooldown = 3000
        self.last_shot = 0
        self.projectile_groups = projectile_groups

    def update(self, platform_rects, delta_time):
        super().update(platform_rects, delta_time)
        self._shoot()

    @abstractmethod
    def _shoot(self):
        pass
