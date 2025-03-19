from settings import *
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from projectiles.spore import Spore
from characters.animation_utils import create_animation_rects
from typing import Optional


class SporePool(ProjectilesPool):
    def __init__(self, size, projectile_groups, game):
        super().__init__(size, projectile_groups, game)

    def _create_pool(self):
        for _ in range(self.size):
            spore = Spore(
                pos=(0, 0),
                surf=pygame.Surface((16, 16)),
                direction=pygame.math.Vector2(-1, 0),
                groups=self.projectile_groups,
                sprite_sheet_name="spore.png",
                animations=create_animation_rects(0, 3, 16),
                game=self.game
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
