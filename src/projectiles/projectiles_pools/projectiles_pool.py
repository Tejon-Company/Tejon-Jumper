from settings import *
from abc import ABC, abstractmethod
from projectiles.projectile import Projectile


class ProjectilesPool(ABC):
    def __init__(self, size, projectile_groups):
        self.pool = list()
        self.size = size
        self.projectile_groups = projectile_groups

    @abstractmethod
    def create_pool(self):
        pass

    @abstractmethod
    def shoot(self, pos_x, pos_y):
        pass
