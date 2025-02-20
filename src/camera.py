from settings import *


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.update_x(target)
        self.update_y(target)

    def update_x(self, target):
        camera_x = -target.rect.centerx + WINDOW_WIDTH // 2
        camera_x = min(0, camera_x)
        camera_x = max(-(self.width - WINDOW_WIDTH), camera_x)
        self.camera.x = camera_x

    def update_y(self, target):
        camera_y = -target.rect.centery + WINDOW_HEIGHT // 2
        camera_y = min(0, camera_y)
        camera_y = max(-(self.height - WINDOW_HEIGHT), camera_y)
        self.camera.y = camera_y
