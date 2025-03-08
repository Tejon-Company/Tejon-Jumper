from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.enemies.enemies_utils import *


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups, sprite_sheet_name):
        super().__init__(pos, surf, groups, sprite_sheet_name)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

        self.animations = create_animation_rects(0, 0, 32, 32, 3, 1)

        self._setup_animation()
