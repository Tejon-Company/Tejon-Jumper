import pygame

from singletons.settings.resolution_settings import ResolutionSettings


class Background:
    """
    Gestiona el fondo del juego con efecto parallax.
    Permite cargar y mostrar imágenes de fondo que se mueven a
    diferentes velocidades según su factor de parallax.
    También maneja automáticamente la repetición del fondo para crear
    un efecto continuo.
    """

    def __init__(self, image_path, pos, parallax_factor):
        self._resolution_settings = ResolutionSettings()
        self._image = pygame.image.load(image_path).convert_alpha()
        self.rect = self._image.get_rect(topleft=pos)
        self._parallax_factor = parallax_factor
        self._offset_x = 0

    def apply_parallax(self, camera_x):
        self.rect.x = (camera_x * self._parallax_factor) + self._offset_x

    def draw(self, surface):
        effective_x = self.rect.x % self._resolution_settings.window_width
        surface.blit(
            self._image,
            (effective_x - self._resolution_settings.window_width, self.rect.y),
        )
        surface.blit(self._image, (effective_x, self.rect.y))
        if effective_x < self._resolution_settings.window_width:
            surface.blit(
                self._image,
                (effective_x + self._resolution_settings.window_width, self.rect.y),
            )
