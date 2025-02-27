from settings import *
from characters.enemies.enemy import Enemy
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from abc import ABC


class Shooter(Enemy, ABC):
    def __init__(self, pos, surf, groups, projectiles_pool=ProjectilesPool):
        super().__init__(pos, surf, groups)
        self.shoot_cooldown = 3000
        self.pos = pos
        self.last_shot = 0
        self.projectiles_pool = projectiles_pool

    def update(self, platform_rects, delta_time):
        self._shoot()

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown and self._is_on_screen():
            self.projectiles_pool.shoot(self.pos[0], self.pos[1])
            self.last_shot = current_time

    def _is_on_screen(self):
        return (0 <= self.rect.x <= WINDOW_WIDTH and
                0 <= self.rect.y <= WINDOW_HEIGHT)
