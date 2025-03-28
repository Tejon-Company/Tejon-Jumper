from singletons.game import Game
from singletons.settings.resolution_settings import ResolutionSettings
from abc import ABC, abstractmethod
from typing import Optional


class ProjectilesPool(ABC):
    """
    Gestiona un conjunto de proyectiles reutilizables para optimizar
    el rendimiento del juego, evitando la creación y destrucción constante de objetos.
    """

    def __init__(self, size, projectile_groups):
        self.resolution_settings = ResolutionSettings()
        self.pool = list()
        self.size = size
        self.projectile_groups = projectile_groups
        self.game = Game()
        self._create_pool()

    @abstractmethod
    def _create_pool(self):
        pass

    @abstractmethod
    def shoot(self, pos_x, pos_y, direction: Optional[tuple] = None):
        pass
