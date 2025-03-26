from singletons.settings import Settings
import pygame


class Camera:
    def __init__(self, width, height):
        self.settings = Settings()
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        camera_x = -target.rect.centerx + self.settings.get_window_width() // 2
        camera_x = min(0, camera_x)
        camera_x = max(-(self.width - self.settings.get_window_width()), camera_x)

        interpolation_factor = 0.055
        self.camera.x += (camera_x - self.camera.x) * interpolation_factor

    def draw_background(self, backgrounds, surface):
        for background in backgrounds:
            background.apply_parallax(self.camera.x)
            background.draw(surface)
