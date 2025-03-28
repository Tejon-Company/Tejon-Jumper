import pygame

from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool


class Squirrel(Shooter):
    """
    Implementa una ardilla enemiga que dispara bellotas al jugador cuando está cerca.
    Se define el comportamiento de disparo y animación.
    """

    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        sprite_sheet_name,
        animations,
        projectiles_pool=AcornPool,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            sprite_sheet_name,
            animations,
            projectiles_pool,
        )
        self.rect = self.image.get_frect(topleft=pos)
        self._is_facing_right = False

    def _update_animation_frame(self, delta_time):
        if self._is_shooting:
            self._shooting_timer += delta_time * 1000

            if self._shooting_timer >= self._shooting_duration:
                self._is_shooting = False
                self._shooting_timer = 0

        self.animation_frame = 1 if self._is_shooting else 0
        self._is_facing_right = False

    def update(self, delta_time):
        super().update(delta_time)
        self._update_direction()

    def _update_direction(self):
        self._is_facing_right = self._player.rect.x > self.rect.x

        if self._is_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        cooldown_passed = current_time - self._last_shot >= self._shoot_cooldown
        is_shooting = cooldown_passed and self._is_player_near()

        if is_shooting:
            self._is_shooting = True
            self._projectiles_pool.shoot(
                self._pos[0],
                self._pos[1],
                self._is_facing_right,
            )
            self._last_shot = current_time
