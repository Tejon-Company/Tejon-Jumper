from characters.sprite import Sprite
from characters.players.player import Player
from abc import ABC, abstractmethod


class Berry(Sprite):
    @abstractmethod
    def update(self, player: Player):
        pass
