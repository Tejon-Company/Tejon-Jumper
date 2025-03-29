from abc import ABC, abstractmethod

from sprites.characters.players.player import Player
from sprites.sprite import Sprite


class Berry(ABC, Sprite):
    """
    Clase abstracta que define una baya.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = surf

        self.rect = self.image.get_frect(topleft=pos)

    @abstractmethod
    def update(self, player: Player):
        pass
