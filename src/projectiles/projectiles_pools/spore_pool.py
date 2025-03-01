from settings import *
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from projectiles.spore import Spore


class SporePool(ProjectilesPool):
    def __init__(self, size, projectile_groups, camera_x):
        super().__init__(size, projectile_groups, camera_x)

    def _create_pool(self):
        for _ in range(self.size):
            spore = Spore(
                pos=(0, 0),
                surf=pygame.Surface((8, 8)),
                direction=pygame.math.Vector2(-1, 0),
                groups=self.projectile_groups,
                camera_x=self.camera_x
            )
            self.pool.append(spore)

    def shoot(self, pos_x, pos_y):
        for spore in self.pool:
            if spore.is_activated:
                continue

            spore.change_position(pos_x, pos_y)
            spore.is_activated = True
            return
