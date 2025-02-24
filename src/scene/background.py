from settings import *


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, speed, parallax_factor, width, groups):
        super().__init__(groups)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.parallax_factor = parallax_factor
        self.width = width
        self.offset_x = 0
        
    def update(self, delta_time):
        self.offset_x -= self.speed * delta_time
        
    def apply_parallax(self, camera_x):
        self.rect.x = (camera_x * self.parallax_factor) + self.offset_x

    def draw(self, surface):
        effective_x = self.rect.x % WINDOW_WIDTH
        surface.blit(self.image, (effective_x - WINDOW_WIDTH, self.rect.y))
        surface.blit(self.image, (effective_x, self.rect.y))
        if effective_x < WINDOW_WIDTH:
            surface.blit(self.image, (effective_x + WINDOW_WIDTH, self.rect.y))