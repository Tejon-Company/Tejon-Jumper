from enum import Enum, auto

import pygame

from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.spore_pool import SporePool


class Mushroom(Shooter):
    """
    Implementa a un enemigo seta que puede detectar al jugador y disparar proyectiles
    en forma de esporas. Tiene tres estados: inactivo, preparándose para disparar y disparando.
    """

    class MushroomState(Enum):
        IDLE = auto()
        PREPARING = auto()
        SHOOTING = auto()

    def __init__(
        self,
        pos,
        surf,
        groups,
        direction,
        player,
        sprite_sheet_name,
        animations,
        projectiles_pool=SporePool,
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
        self.direction = direction
        self._shoot_cooldown = 5000
        self.rect = self.image.get_frect(topleft=pos)

        self._pre_shoot_duration = 500
        self._shooting_duration = 300

        self._current_state = self.MushroomState.IDLE
        self._state_timer = 0

    def update(self, delta_time):
        super().update(delta_time)

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        had_cooldown_passed = current_time - self._last_shot >= self._shoot_cooldown

        if had_cooldown_passed and self._is_player_near():
            self._current_state = self.MushroomState.PREPARING
            self._state_timer = 0
            self._last_shot = current_time

    def _update_animation_frame(self, delta_time):
        delta_ms = delta_time * 1000

        if self._current_state == self.MushroomState.PREPARING:
            self._handle_preparing_state(delta_ms)
        elif self._current_state == self.MushroomState.SHOOTING:
            self._handle_shooting_state(delta_ms)
        else:
            self.animation_frame = 0

    def _handle_preparing_state(self, delta_ms):
        self._state_timer += delta_ms
        self.animation_frame = 1
        is_ready_to_shoot = self._state_timer >= self._pre_shoot_duration

        if is_ready_to_shoot:
            self._current_state = self.MushroomState.SHOOTING
            self._state_timer = 0

    def _handle_shooting_state(self, delta_ms):
        self._state_timer += delta_ms
        is_shooting_ready = self._state_timer >= self._shooting_duration

        if is_shooting_ready:
            self._projectiles_pool.shoot(
                self._pos[0],
                self._pos[1],
                self.direction,
            )
            self._current_state = self.MushroomState.IDLE
            self._state_timer = 0
        else:
            is_ready_for_next_frame = self._state_timer >= self._shooting_duration * 0.1
            self.animation_frame = 2 if is_ready_for_next_frame else 1
