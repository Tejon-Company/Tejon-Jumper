from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool


class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, player, sprite_sheet_name, animations, projectiles_pool=AcornPool):
        super().__init__(pos, surf, groups, player,
                         sprite_sheet_name, animations, projectiles_pool)

        self.rect = self.image.get_frect(topleft=pos)

        self._setup_animation()

    def _update_animation_frame(self, delta_time):
        if self.is_shooting:
            self.shooting_timer += delta_time * 1000
            if self.shooting_timer >= self.shooting_duration:
                self.is_shooting = False
                self.shooting_timer = 0
        self.animation_frame = 1 if self.is_shooting else 0
