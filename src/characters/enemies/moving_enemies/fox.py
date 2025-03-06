from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from os.path import join


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

        self.sprite_sheet_path = join(
            "assets", "creatures_and_else", "enemies", "with_background", "fox.png")

        pixel_gap_between_sprites = 1
        self.animations = Fox.create_animation_rects()

        self._setup_animation()

    def create_animation_rects(start_x=0, y=0, width=32, height=32, frames=3, pixel_gap=1):
        animation_rects = []
        for i in range(frames):
            x = start_x + (width * i) + (i * pixel_gap)
            animation_rects.append((x, y, width, height))
        return animation_rects

    def update(self, platform_rects, delta_time):
        super().update(platform_rects, delta_time)

        self.facing_right = self.direction > 0
        self._update_animation(delta_time)
