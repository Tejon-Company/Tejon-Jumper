from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT)) 
        self.rect = self.image.get_rect(topleft=pos)
