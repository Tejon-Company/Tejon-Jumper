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
        self.resolution_settings = ResolutionSettings()
        self.update_display_surface_resolution()
        pygame.display.set_caption("Tejón Jumper")

        self.stack = []
        self.exit_scene = False
        self.clock = pygame.time.Clock()

    def update_display_surface_resolution(self):
        self.display_surface = pygame.display.set_mode(
            (
                self.resolution_settings.window_width,
                self.resolution_settings.window_height,
            )
        )

    def _loop(self, scene):
        self.exit_scene = False
        pygame.event.clear()

        while not self.exit_scene:
            delta_time = self.clock.tick(60) / 1000
            scene.events(pygame.event.get())
            scene.update(
                delta_time,
            )
            scene.draw(self.display_surface)

            pygame.display.update()
            pygame.display.flip()

    def run(self):
        while len(self.stack) > 0:
            scene = self.stack[-1]
            self._loop(scene)

    def pop_scene(self):
        ResourceManager.clear_resources()
        self.exit_scene = True
        if len(self.stack) > 0:
            current_scene = self.stack.pop()
            return current_scene

    def exit_program(self):
        ResourceManager.clear_resources()
        self.stack = []
        self.exit_scene = True

    def change_scene(self, scene):
        ResourceManager.clear_resources()
        self.pop_scene()
        self.stack.append(scene)

    def push_scene(self, scene):
        self.exit_scene = True
        self.stack.append(scene)
