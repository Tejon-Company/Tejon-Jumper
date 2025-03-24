from abc import ABC, abstractmethod
from scene.scene import Scene
from settings import *
from resource_manager import ResourceManager


class Menu(Scene, ABC):
    def __init__(self, director):
        super().__init__(director)
        self.click_button_sound = ResourceManager.load_sound_effect("click_button.ogg")

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    @abstractmethod
    def _mouse_button_down(self, event):
        pass
