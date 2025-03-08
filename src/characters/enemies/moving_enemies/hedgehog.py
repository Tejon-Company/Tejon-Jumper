from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice


class Hedgehog(MovingEnemy):
    def __init__(self, pos, surf, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, sprite_sheet_name, animations)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 50

        self._setup_animation()
