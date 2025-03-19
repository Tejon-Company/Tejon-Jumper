from settings import *
from characters.players.player import Player
from berries.berry import Berry


class EneryBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, game, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        player.recover_energy()
        self.kill()
