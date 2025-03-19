from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from characters.animation_utils import setup_animation
from random import choice


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, player,
                         platform_rects, sprite_sheet_name, animations, game)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

        setup_animation(self)
