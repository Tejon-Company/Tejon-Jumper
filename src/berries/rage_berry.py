from berries.berry import Berry
from characters.players.player import Player


class RageBerry(Berry):
    """
    Implementa una baya que activa el estado de rabia en el jugador cuando este colisiona con ella.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        player.activate_rage()
        self.kill()
