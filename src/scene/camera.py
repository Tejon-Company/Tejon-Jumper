import pygame

from singletons.settings.resolution_settings import ResolutionSettings


class Camera:
    """
    Implementa la cámara que sigue al jugador en el juego. Controla qué parte del mundo de juego
    es visible en la pantalla en un momento dado.
    La cámara sigue al objetivo (generalmente el jugador) con una interpolación suave,
    y aplica un desplazamiento a todas las entidades del juego para crear la ilusión de movimiento.
    También maneja el dibujo de fondos con efecto parallax.
    """

    def __init__(self, width, height):
        self._resolution_settings = ResolutionSettings()
        self._camera = pygame.Rect(0, 0, width, height)
        self._width = width

    def apply(self, entity):
        return entity.rect.move(self._camera.topleft)

    def update(self, target):
        camera_x = -target.rect.centerx + self._resolution_settings.window_width // 2
        camera_x = min(0, camera_x)
        camera_x = max(-(self._width - self._resolution_settings.window_width), camera_x)

        interpolation_factor = 0.055
        self._camera.x += (camera_x - self._camera.x) * interpolation_factor

    def draw_background(self, backgrounds, surface):
        for background in backgrounds:
            background.apply_parallax(self._camera.x)
            background.draw(surface)
