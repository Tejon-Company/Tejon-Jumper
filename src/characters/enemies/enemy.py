from settings import *
from characters.character import Character
from abc import ABC, abstractmethod
from characters.players.player import Player
from characters.enemies.enemy_collision_directions import CollisionDirection
from characters.players.collision_utils import is_above_collision, is_below_collision, is_left_collision, is_right_collision

class Enemy(Character):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.groups = groups

    def handle_collision_with_player(self, player):
        pass

    def defeat(self):
        for group in self.groups:
            if self in group:
                group.remove(self)
        self.kill()
        

    def get_collision_direction(self, player):
        player_rect = player.rect
        player_old_rect = player.old_rect  # Se asume que `old_rect` almacena la posición anterior del jugador

        if is_right_collision(player_rect, player_old_rect, self.rect):
            return CollisionDirection.RIGHT
        elif is_left_collision(player_rect, player_old_rect, self.rect):
            return CollisionDirection.LEFT
        elif is_above_collision(player_rect, player_old_rect, self.rect):
            return CollisionDirection.ABOVE
        elif is_below_collision(player_rect, player_old_rect, self.rect):
            return CollisionDirection.BELOW

        return CollisionDirection.NONE  # Si no hay colisión


    def adjust_player_position(self, player):
        if player.rect.colliderect(self.rect):

            if player.rect.centerx < self.rect.centerx:
                player.rect.right = self.rect.left

            else:
                player.rect.left = self.rect.right

        if player.rect.colliderect(self.rect):
            if player.rect.centery < self.rect.centery:

                player.rect.bottom = self.rect.top
            else:

                player.rect.top = self.rect.bottom

