from settings import *


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, speed, groups):
        super().__init__(groups)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        
    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time
        if abs(self.rect.topleft) > WINDOW_WIDTH:
            self.rect.topleft = 0
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.rect.right < WINDOW_WIDTH:
            surface.blit(self.image, (self.rect.right, self.rect.top))
