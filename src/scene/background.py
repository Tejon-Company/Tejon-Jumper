from singletons.settings.resolution_settings import ResolutionSettings
import pygame


class Background:
    """
    Gestiona el fondo del juego con efecto parallax.
    Permite cargar y mostrar imágenes de fondo que se mueven a
    diferentes velocidades según su factor de parallax.
    También maneja automáticamente la repetición del fondo para crear
    un efecto continuo.
    """

    def __init__(self, image_path, pos, parallax_factor):
        self.resolution_settings = ResolutionSettings()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.parallax_factor = parallax_factor
        self.offset_x = 0

    def apply_parallax(self, camera_x):
        self.rect.x = (camera_x * self.parallax_factor) + self.offset_x

    def draw(self, surface):
        effective_x = self.rect.x % self.resolution_settings.window_width
        surface.blit(
            self.image,
            (effective_x - self.resolution_settings.window_width, self.rect.y),
        )
        surface.blit(self.image, (effective_x, self.rect.y))
        if effective_x < self.resolution_settings.window_width:
            surface.blit(
                self.image,
                (effective_x + self.resolution_settings.window_width, self.rect.y),
            )
