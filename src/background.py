from settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT)) 
        self.rect = self.image.get_rect(topleft=pos)
