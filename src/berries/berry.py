from characters.sprite import Sprite
from characters.players.player import Player
from abc import ABC, abstractmethod


class Berry(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = surf

        self.rect = self.image.get_frect(topleft=pos)

    @abstractmethod
    def update(self, player: Player):
        pass
