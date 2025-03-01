from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.spore_pool import SporePool


class Mushroom(Shooter):
    def __init__(self, pos, surf, groups, player, projectiles_pool=SporePool):
        super().__init__(pos, surf, groups, player, projectiles_pool)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="pink")

        self.rect = self.image.get_frect(topleft=pos)
