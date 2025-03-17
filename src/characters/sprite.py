from settings import *
from resource_manager import ResourceManager


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, sprite_sheet_name):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.sprite_sheet = ResourceManager.load_sprite_sheet(
            sprite_sheet_name)
