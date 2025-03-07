from settings import *
from characters.character import Character


class Enemy(Character):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def _setup_animation(self):
        self.sprite_sheet = pygame.image.load(
            self.sprite_sheet_path).convert_alpha()
        self.image = self.sprite_sheet.subsurface((0, 0, 32, 32))
        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0
