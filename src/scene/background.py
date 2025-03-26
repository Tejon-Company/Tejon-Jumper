from singletons.settings import Settings
import pygame


class Background:
    def __init__(self, image_path, pos, parallax_factor):
        self.settings = Settings()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.parallax_factor = parallax_factor
        self.offset_x = 0

    def apply_parallax(self, camera_x):
        self.rect.x = (camera_x * self.parallax_factor) + self.offset_x

    def draw(self, surface):
        effective_x = self.rect.x % self.settings.get_window_width()
        surface.blit(
            self.image, (effective_x - self.settings.get_window_width(), self.rect.y)
        )
        surface.blit(self.image, (effective_x, self.rect.y))
        if effective_x < self.settings.get_window_width():
            surface.blit(
                self.image, (effective_x + self.settings.get_window_width(), self.rect.y)
            )
