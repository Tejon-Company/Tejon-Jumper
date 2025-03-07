from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.enemies.enemies_utils import *


class Hedgehog(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 50

        self.sprite_sheet_path = join(
            "assets", "creatures_and_else", "enemies", "with_background", "hedgehog.png")

        self.animations = create_animation_rects(0, 0, 32, 32, 2, 1)

        self._setup_animation()
