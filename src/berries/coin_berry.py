from berries.berry import Berry
from characters.players.player import Player
from resource_manager import ResourceManager
from singletons.game import Game


class CoinBerry(Berry):
    """
    Implementa una baya de tipo moneda que el jugador puede recolectar.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self._get_coin_sound = ResourceManager.load_sound_effect("get_coin.ogg")
        self._game = Game()

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self._get_coin_sound.play()
        self._game.add_coin()
        self.kill()
