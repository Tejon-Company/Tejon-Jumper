from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool


class Squirrel(Shooter):
    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        sprite_sheet_name,
        animations,
        game,
        projectiles_pool=AcornPool,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            sprite_sheet_name,
            animations,
            game,
            projectiles_pool,
        )
        self.rect = self.image.get_frect(topleft=pos)

    def _update_animation_frame(self, delta_time):
        if self.is_shooting:
            self.shooting_timer += delta_time * 1000

            if self.shooting_timer >= self.shooting_duration:
                self.is_shooting = False
                self.shooting_timer = 0

        self.animation_frame = 1 if self.is_shooting else 0
        self._is_facing_right = False

    def update(self, delta_time):
        super().update(delta_time)
        self._update_direction()

    def _update_direction(self):
        self._is_facing_right = self.player.rect.x > self.rect.x

        if self._is_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        cooldown_passed = current_time - self.last_shot >= self.shoot_cooldown
        is_shooting = cooldown_passed and self._is_player_near()

        if is_shooting:
            self.is_shooting = True
            self.projectiles_pool.shoot(self.pos[0], self.pos[1], self._is_facing_right, )
            self.last_shot = current_time
