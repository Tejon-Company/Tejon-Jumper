from berries.berry import Berry
from characters.players.player import Player
from resource_manager import ResourceManager
from singletons.game import Game


class CoinBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.get_coin_sound = ResourceManager.load_sound_effect("get_coin.ogg")
        self.game = Game()

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self.get_coin_sound.play()
        self.game.add_coin()
        self.kill()
