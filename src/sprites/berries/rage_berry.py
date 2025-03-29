from sprites.berries.berry import Berry
from sprites.characters.players.player import Player


class RageBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        player.activate_rage()
        self.kill()
