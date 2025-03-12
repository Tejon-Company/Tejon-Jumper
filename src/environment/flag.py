from settings import *
from characters.players.player import Player
from environment.environment_element import EnvironmentElement


class Flag(EnvironmentElement):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, player: Player):
        if self.rect.colliderect(player.rect):
            self.kill()
