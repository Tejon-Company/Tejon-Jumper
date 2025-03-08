from settings import *
from characters.character import Character


class Enemy(Character):
    def __init__(self, pos, surf, groups, sprite_sheet_name):
        super().__init__(pos, surf, groups, sprite_sheet_name)

    def _setup_animation(self):
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0
