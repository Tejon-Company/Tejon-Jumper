from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool


class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, projectiles_pool=AcornPool):
        super().__init__(pos, surf, groups, projectiles_pool)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="brown")

        self.rect = self.image.get_frect(topleft=pos)
