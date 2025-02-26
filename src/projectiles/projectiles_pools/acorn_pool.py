from settings import *
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from projectiles.acorn import Acorn


class AcornPool(ProjectilesPool):
    def __init__(self, size, projectile_groups):
        super().__init__(size, projectile_groups)

    def create_pool(self):
        for _ in range(self.size):
            acorn = Acorn(
                pos=(0, 0),
                surf=pygame.Surface((8, 8)),
                direction=pygame.math.Vector2(-1, 0),
                groups=self.projectile_groups,
            )
            self.pool.append(acorn)

    def shoot(self, pos_x, pos_y):
        for acorn in self.pool:
            if acorn.is_activated:
                continue
            else:
                acorn.change_position(pos_x, pos_y)
                acorn.is_activated = True
                break
