from settings import *
from characters.enemies.enemy import Enemy
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from abc import ABC


class Shooter(Enemy, ABC):
    def __init__(self, pos, surf, groups, player, projectiles_pool=ProjectilesPool):
        super().__init__(pos, surf, groups)
        self.shoot_cooldown = 3000
        self.pos = pos
        self.last_shot = 0
        self.player = player
        self.projectiles_pool = projectiles_pool
        self.is_shooting = False

    def update(self, platform_rects, delta_time):
        self._shoot()

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        cooldown_passed = current_time - self.last_shot >= self.shoot_cooldown
        is_shooting = cooldown_passed and self._is_player_near()

        if is_shooting:
            self.is_shooting = True
            self.projectiles_pool.shoot(self.pos[0], self.pos[1])
            self.last_shot = current_time

    def _is_player_near(self):
        player_pos, projectile_pos = vector(
            self.player.rect.center), vector(self.rect.center)
        return projectile_pos.distance_to(player_pos) < 500
