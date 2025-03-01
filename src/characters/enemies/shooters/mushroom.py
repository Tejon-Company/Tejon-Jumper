from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.spore_pool import SporePool


class Mushroom(Shooter):
    def __init__(self, pos, surf, groups, projectiles_pool=SporePool):
        super().__init__(pos, surf, groups, projectiles_pool)

        self.rect = self.image.get_frect(topleft=pos)
