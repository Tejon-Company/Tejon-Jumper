from sprites.sprite import Sprite
from abc import ABC


class EnvironmentElement(Sprite, ABC):
    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
