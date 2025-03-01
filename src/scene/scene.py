from abc import ABC, abstractmethod
from director import Director


class Scene(ABC):
    def __init__(self, director: Director):
        self.director = director

    def update(self, delta_time):
        pass

    @abstractmethod
    def events(self, events_list):
        pass

    @abstractmethod
    def draw(self, display_surface):
        pass
