from settings import *
from characters.character import Character
from abc import ABC, abstractmethod
from characters.players.player import Player
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

    def adjust_player_position(self, player):
        if player.rect.colliderect(self.rect):  
            if abs(player.rect.centerx - self.rect.centerx) > abs(player.rect.centery - self.rect.centery):
                
                if player.rect.centerx < self.rect.centerx:
                    player.rect.right = self.rect.left
                else:
                    player.rect.left = self.rect.right
            else:
                
                if player.rect.centery < self.rect.centery:
                    player.rect.bottom = self.rect.top
                else:
                    player.rect.top = self.rect.bottom
