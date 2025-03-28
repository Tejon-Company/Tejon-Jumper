import pygame

from resource_manager import ResourceManager
from singletons.settings.resolution_settings import ResolutionSettings
from singletons.singleton_meta import SingletonMeta


class Director(metaclass=SingletonMeta):
    """
    Gestiona el juego. Controla su flujo, maneja la pila de escenas,
    actualiza la pantalla y maneja la resolución del juego.
    """

    def __init__(self):
        self._resolution_settings = ResolutionSettings()
        self.update_display_surface_resolution()
        pygame.display.set_caption("Tejón Jumper")

        self._stack = []
        self._exit_scene = False
        self._clock = pygame.time.Clock()

    def update_display_surface_resolution(self):
        self._display_surface = pygame.display.set_mode(
            (
                self._resolution_settings.window_width,
                self._resolution_settings.window_height,
            )
        )

    def _loop(self, scene):
        self._exit_scene = False
        pygame.event.clear()

        while not self._exit_scene:
            delta_time = self._clock.tick(60) / 1000
            scene.events(pygame.event.get())
            scene.update(
                delta_time,
            )
            scene.draw(self._display_surface)

            pygame.display.update()
            pygame.display.flip()

    def run(self):
        while len(self._stack) > 0:
            scene = self._stack[-1]
            self._loop(scene)

    def pop_scene(self):
        ResourceManager.clear_resources()
        self._exit_scene = True
        if len(self._stack) > 0:
            current_scene = self._stack.pop()
            return current_scene

    def exit_program(self):
        ResourceManager.clear_resources()
        self._stack = []
        self._exit_scene = True

    def change_scene(self, scene):
        ResourceManager.clear_resources()
        self.pop_scene()
        self._stack.append(scene)

    def push_scene(self, scene):
        self._exit_scene = True
        self._stack.append(scene)
