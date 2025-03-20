from settings import *
from characters.players.player import Player
from berries.berry import Berry
from resource_manager import ResourceManager


class CoinBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.get_coin_sound = ResourceManager.load_sound("get_coin.ogg")

    def update(self, game, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self.get_coin_sound.play()
        game.add_coin()
        self.kill()
