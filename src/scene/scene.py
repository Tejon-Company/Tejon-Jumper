from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, director):
        self.director = director

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def events(self, events_list):
        pass

    @abstractmethod
    def draw(self, display_surface):
        pass
