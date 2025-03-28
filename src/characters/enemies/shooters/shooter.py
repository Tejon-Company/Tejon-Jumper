from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2 as vector

from characters.enemies.enemy import Enemy
from characters.utils.animation_utils import set_animation_parameters
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool


class Shooter(Enemy, ABC):
    """
    Clase abstracta para enemigos que disparan al jugador.
    Implementa la capacidad de disparar proyectiles cuando el jugador está cerca,
    un sistema de enfriamiento entre disparos y gestión de animaciones para
    representar visualmente la acción de disparar.
    """

    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        sprite_sheet_name,
        animations,
        projectiles_pool=ProjectilesPool,
    ):
        super().__init__(pos, surf, groups, player, None, sprite_sheet_name, animations)
        self._shoot_cooldown = 3000
        self._pos = pos
        self._last_shot = 0
        self._player = player
        self._projectiles_pool = projectiles_pool
        self._is_shooting = False
        self._shooting_timer = 0
        self._shooting_duration = 500
        set_animation_parameters(self)

    def update(self, delta_time):
        super().update(delta_time)
        self._shoot()
        self._update_animation_frame(delta_time)
        self.update_sprite()

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        cooldown_passed = current_time - self._last_shot >= self._shoot_cooldown
        is_shooting = cooldown_passed and self._is_player_near()

        if is_shooting:
            self._is_shooting = True
            self._projectiles_pool.shoot(self._pos[0], self._pos[1])
            self._last_shot = current_time

    def _is_player_near(self):
        player_pos = vector(self._player.rect.center)
        projectile_pos = vector(self.rect.center)

        return projectile_pos.distance_to(player_pos) < 500

    @abstractmethod
    def _update_animation_frame(self, delta_time):
        pass

    def update_sprite(self):
        frame_rect = self._animations[self.animation_frame]
        self.image = self._sprite_sheet.subsurface(frame_rect)
