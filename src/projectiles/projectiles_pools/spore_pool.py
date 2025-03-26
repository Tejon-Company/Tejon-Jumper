from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from projectiles.spore import Spore
from characters.utils.animation_utils import create_animation_rects
from typing import Optional
import pygame


class SporePool(ProjectilesPool):
    def __init__(self, size, projectile_groups):
        super().__init__(size, projectile_groups)

    def _create_pool(self):
        spore_size = self.settings.get_tile_size() / 2
        for _ in range(self.size):
            spore = Spore(
                pos=(0, 0),
                surf=pygame.Surface((spore_size, spore_size)),
                direction=pygame.math.Vector2(-1, 0),
                groups=self.projectile_groups,
                sprite_sheet_name="spore.png",
                animations=create_animation_rects(
                    0, 3, sprite_height=16, sprite_width=16
                ),
            )
            self.pool.append(spore)

    def shoot(self, pos_x, pos_y, direction: Optional[tuple] = None):
        for spore in self.pool:
            if spore.is_activated:
                continue

            spore.change_position(pos_x, pos_y)
            if direction is not None:
                spore.change_direction(direction)
            spore.is_activated = True
            return
