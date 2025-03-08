from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool
from characters.enemies.enemies_utils import *


class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, player, sprite_sheet_name, projectiles_pool=AcornPool):
        super().__init__(pos, surf, groups, player, sprite_sheet_name, projectiles_pool)

        self.rect = self.image.get_frect(topleft=pos)

        self.animations = create_animation_rects(32, 0, 32, 32, 2, 1)

        self._setup_animation()

    def update(self, platform_rects, delta_time):
        self._update_animation(delta_time)
        super().update(platform_rects, delta_time)

    def _update_animation(self, delta_time):
        self._update_animation_frame(delta_time)
        self._update_sprite()

    def _update_animation_frame(self, delta_time):
        if self.is_shooting:
            self.shooting_timer += delta_time * 1000
            if self.shooting_timer >= self.shooting_duration:
                self.is_shooting = False
                self.shooting_timer = 0
        self.animation_frame = 1 if self.is_shooting else 0

    def _update_sprite(self):
        frame_rect = self.animations[self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)
