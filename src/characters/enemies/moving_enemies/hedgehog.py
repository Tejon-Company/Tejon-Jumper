from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.players.player_state import PlayerState
from characters.players.collision_utils import is_below_collision
from pygame.sprite import collide_rect


class Hedgehog(MovingEnemy):
    def __init__(self, pos, surf, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, sprite_sheet_name, animations)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 50

        self._setup_animation()

    def _handle_collision_with_player(self, level, player):
        if not collide_rect(self, player):
            return

        self._adjust_player_position(player)

        is_player_falling_on_enemy = is_below_collision(
            player.rect, player.old_rect, self.rect)

        if not is_player_falling_on_enemy and player.is_sprinting:
            self._defeat()
            return
        if player.receive_damage() == PlayerState.DEAD:
            level.handle_dead()
