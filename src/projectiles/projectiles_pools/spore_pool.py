from typing import Optional

import pygame

from characters.utils.animation_utils import create_animation_rects
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from projectiles.spore import Spore


class SporePool(ProjectilesPool):
    """
    Clase que gestiona un grupo de esporas reutilizables.
    Permite crear, almacenar y disparar esporas desde una posición específica
    en una dirección determinada.
    """

    def __init__(self, size, projectile_groups):
        super().__init__(size, projectile_groups)

    def _create_pool(self):
        spore_size = self._resolution_settings.tile_size / 2
        for _ in range(self._size):
            spore = Spore(
                (0, 0),
                pygame.Surface((spore_size, spore_size)),
                pygame.math.Vector2(-1, 0),
                self._projectile_groups,
                "spore.png",
                create_animation_rects(
                    0,
                    3,
                    sprite_height=self._resolution_settings.tile_size // 2,
                    sprite_width=self._resolution_settings.tile_size // 2,
                ),
            )
            self._pool.append(spore)

    def shoot(self, pos_x, pos_y, direction: Optional[tuple] = None):
        for spore in self._pool:
            if spore.is_activated:
                continue

            spore.change_position(pos_x, pos_y)
            if direction is not None:
                spore.change_direction(direction)
            spore.is_activated = True
            return
