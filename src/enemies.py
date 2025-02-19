from settings import *

class Zorro(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="green")
        
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        
        self.collision_sprites = collision_sprites
        self.on_surface = False
        
    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        
    
        