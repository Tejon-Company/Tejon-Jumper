from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.players.collision_utils import is_below_collision
from pygame.sprite import collide_rect


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups, platform_rects, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, platform_rects, sprite_sheet_name, animations)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

        self._setup_animation()