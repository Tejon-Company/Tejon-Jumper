from settings import *
from random import choice

class Fox(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="green")
        
        self.rect = self.image.get_frect(topleft=pos)
        
        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 75
        
    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        
    def _move(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time
        # Reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1,1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1,1))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
        floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
            self.direction *= -1
    
    