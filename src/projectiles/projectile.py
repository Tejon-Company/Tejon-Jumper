from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite
from characters.players.collision_utils import is_below_collision
from pygame.sprite import collide_rect


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, groups, game):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.game = game
        self.speed = None
        self.is_activated = False

    def update(self, delta_time, player):
        if not self.is_activated:
            return

        self._reset_projectile_if_off_screen()
        self.old_rect = self.rect.copy()
        self._move(delta_time)

        self._handle_collision_with_player(player)

    @abstractmethod
    def _reset_projectile_if_off_screen(self):
        pass

    @abstractmethod
    def _move(self, delta_time):
        pass

    def _handle_collision_with_player(self, player):
        if not collide_rect(self, player):
            return

        is_player_colliding_from_above = is_below_collision(
            player.rect, player.old_rect, self.rect)

        if is_player_colliding_from_above or player.is_sprinting:
            self._deactivate_projectile()
            return

        self.game.receive_damage()
        self._deactivate_projectile()

    @abstractmethod
    def _deactivate_projectile(self):
        pass

    @abstractmethod
    def change_position(self, new_pos_x, new_pos_y):
        pass
