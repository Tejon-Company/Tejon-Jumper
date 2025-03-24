from settings import *


class Background:
    def __init__(self, image_path, pos, parallax_factor):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)
        self.parallax_factor = parallax_factor
        self.offset_x = 0

    def apply_parallax(self, camera_x):
        self.rect.x = (camera_x * self.parallax_factor) + self.offset_x

    def draw(self, surface):
        effective_x = self.rect.x % WINDOW_WIDTH
        surface.blit(self.image, (effective_x - WINDOW_WIDTH, self.rect.y))
        surface.blit(self.image, (effective_x, self.rect.y))
        if effective_x < WINDOW_WIDTH:
            surface.blit(self.image, (effective_x + WINDOW_WIDTH, self.rect.y))
