from abc import ABC, abstractmethod
from singletons.director import Director
from resource_manager import ResourceManager
from pygame.mixer import music


class Scene(ABC):
    """
    Clase abstracta que define la estructura base para todas las escenas del juego.
    Proporciona un marco para gestionar escenas individuales,
    incluyendo la configuración de música, actualización de lógica y renderizado.
    """

    def __init__(self):
        self.director = Director()

    @staticmethod
    def _setup_music(music_name):
        music_file = ResourceManager.load_music(music_name)
        music.load(music_file)
        music.play(-1)

    def update(self, delta_time):
        pass

    @abstractmethod
    def events(self, events_list):
        pass

    @abstractmethod
    def draw(self, display_surface):
        pass
