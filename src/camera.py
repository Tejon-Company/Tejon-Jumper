from settings import *


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        camera_x = -target.rect.centerx + WINDOW_WIDTH // 2
        camera_x = min(0, camera_x)
        camera_x = max(-(self.width - WINDOW_WIDTH), camera_x)
        self.camera.x = camera_x
