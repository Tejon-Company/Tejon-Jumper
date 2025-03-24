from settings import *
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from projectiles.acorn import Acorn
from characters.utils.animation_utils import create_animation_rects
from singletons.game import Game
from typing import Optional


class AcornPool(ProjectilesPool):
    def __init__(self, size, projectile_groups):
        super().__init__(size, projectile_groups)

    def _create_pool(self):
        for _ in range(self.size):
            acorn = Acorn(
                pos=(0, 0),
                surf=pygame.Surface((16, 16)),
                direction=pygame.math.Vector2(-1, 0),
                groups=self.projectile_groups,
                sprite_sheet_name="acorn.png",
                animations=create_animation_rects(
                    0, 8, sprite_height=16, sprite_width=16),
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
