from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from os.path import join
from characters.enemies.enemies_utils import *
from resource_manager import ResourceManager


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

        self.sprite_sheet = ResourceManager.load_sprite("fox.png")
        self.animations = create_animation_rects(0, 0, 32, 32, 3, 1)

        self._setup_animation()
