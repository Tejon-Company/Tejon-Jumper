from typing import Optional

import pygame

from sprites.characters.utils.animation_utils import create_animation_rects
from sprites.projectiles.acorn import Acorn
from sprites.projectiles.projectiles_pools.projectiles_pool import ProjectilesPool


class AcornPool(ProjectilesPool):
    """
    Clase que gestiona un grupo de bellotas reutilizables. Permite
    crear, almacenar y disparar bellotaas desde una posición específica
    en una dirección determinada.
    """

    def __init__(self, size, projectile_groups):
        super().__init__(size, projectile_groups)

    def _create_pool(self):
        acorn_size = self.resolution_settings.tile_size / 2
        for _ in range(self.size):
            acorn = Acorn(
                (0, 0),
                pygame.Surface((acorn_size, acorn_size)),
                pygame.math.Vector2(-1, 0),
                self.projectile_groups,
                "acorn.png",
                create_animation_rects(
                    0,
                    8,
                    sprite_height=self.resolution_settings.tile_size // 2,
                    sprite_width=self.resolution_settings.tile_size // 2,
                ),
            )
            self.pool.append(acorn)

    def shoot(self, pos_x, pos_y, is_facing_right, direction: Optional[tuple] = None):
        for acorn in self.pool:
            if acorn.is_activated:
                continue
            acorn.set_facing_right(is_facing_right)
            acorn.change_position(pos_x, pos_y)
            acorn.is_activated = True
            return
