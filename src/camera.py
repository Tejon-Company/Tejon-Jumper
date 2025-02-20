from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft).move(0, 200)

    def update(self, target):
        camera_x = -target.rect.centerx + WINDOW_WIDTH // 2
        camera_y = -target.rect.centery + WINDOW_HEIGHT // 2

        camera_x = min(0, camera_x)  
        camera_y = min(0, camera_y)  
        camera_x = max(-(self.width - WINDOW_WIDTH), camera_x) 
        camera_y = max(-(self.height - WINDOW_HEIGHT), camera_y) 

        self.camera = pygame.Rect(camera_x, camera_y, self.width, self.height)
