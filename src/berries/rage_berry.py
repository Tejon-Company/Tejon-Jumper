from settings import *
from characters.players.player import Player
from berries.berry import Berry


class RageBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        # player.rage()
        self.kill()
