from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.spore_pool import SporePool
from characters.players.player_state import PlayerState


class Mushroom(Shooter):
    def __init__(self, pos, surf, groups, direction, player, sprite_sheet_name, animations, projectiles_pool=SporePool):
        super().__init__(pos, surf, groups, player,
                         sprite_sheet_name, animations, projectiles_pool)
        self.direction = direction
        self.shoot_cooldown = 5000
        self.rect = self.image.get_frect(topleft=pos)

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        cooldown_passed = current_time - self.last_shot >= self.shoot_cooldown
        is_shooting = cooldown_passed and self._is_player_near()

        if is_shooting:
            self.is_shooting = True
            self.projectiles_pool.shoot(self.pos[0], self.pos[1], self.direction)
            self.last_shot = current_time
