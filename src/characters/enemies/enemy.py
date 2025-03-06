from settings import *
from characters.character import Character
from abc import ABC, abstractmethod
from characters.players.player import Player


class Enemy(Character):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.groups = groups

    @abstractmethod
    def handle_collision_with_player(self, player):
        pass
    @abstractmethod
    def defeat(self):
        pass
    def get_collision_direction(self, player):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        if abs(dx) > abs(dy):
            return "izquierda" if dx > 0 else "derecha"
        else:
            return "arriba" if dy > 0 else "abajo"

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

