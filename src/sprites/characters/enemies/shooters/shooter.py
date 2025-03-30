from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2 as vector

from sprites.characters.enemies.enemy import Enemy
from sprites.characters.utils.animation_utils import set_animation_parameters
from sprites.projectiles.projectiles_pools.projectiles_pool import ProjectilesPool


class Shooter(Enemy, ABC):
    """
    Clase abstracta para enemigos que disparan al jugador. Implementa la
    capacidad de disparar proyectiles cuando el jugador está cerca, un
    sistema de enfriamiento entre disparos y gestión de animaciones para
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
        self.shoot_cooldown = 3000
        self.pos = pos
        self.last_shot = 0
        self.player = player
        self.projectiles_pool = projectiles_pool
        self.is_shooting = False
        self.shooting_timer = 0
        self.shooting_duration = 500
        set_animation_parameters(self)

    def update(self, delta_time):
        super().update(delta_time)
        self._shoot()
        self._update_animation_frame(delta_time)
        self._update_sprite()

    @abstractmethod
    def _shoot(self):
        pass

    def _is_player_near(self):
        player_pos = vector(self.player.rect.center)
        projectile_pos = vector(self.rect.center)

        return projectile_pos.distance_to(player_pos) < 500 * self._ratio

    @abstractmethod
    def _update_animation_frame(self, delta_time):
        pass

    def _update_sprite(self):
        frame_rect = self.animations[self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)
