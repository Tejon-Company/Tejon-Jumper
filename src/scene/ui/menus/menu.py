from abc import ABC, abstractmethod

import pygame

from resource_manager import ResourceManager
from scene.scene import Scene


class Menu(Scene, ABC):
    """
    Clase abstracta que implementa un menú en el juego. Proporciona una
    estructura base para todos los menús del juego, gestionando eventos
    de entrada como clics de ratón y salida del programa.
    """

    def __init__(self):
        super().__init__()
        self.click_button_sound = ResourceManager.load_sound_effect("click_button.ogg")

    def events(self, events_list):
        for event in events_list:
            self._handle_event(event)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.director.exit_program()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_button_down(event.pos)

    @abstractmethod
    def _mouse_button_down(self, event):
        pass
