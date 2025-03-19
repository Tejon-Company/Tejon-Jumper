from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.players.collision_utils import is_below_collision
from pygame.sprite import collide_rect


class Hedgehog(MovingEnemy):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 50

        self._setup_animation()

    def _handle_collision_with_player(self):
        if not collide_rect(self, self.player):
            return

        self._adjust_player_position()
        is_below = is_below_collision(self.player.rect, self.player.old_rect, self.rect)

        if self.player.is_sprinting and not is_below:
            self.defeat()
            return

        self.game.receive_damage()
