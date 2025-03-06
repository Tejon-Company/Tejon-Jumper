from settings import *
from characters.players.player import Player
from berries.berry import Berry
from resource_manager import ResourceManager


class CoinBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = pygame.Surface((32, 32))
        self.image.fill("purple")

        self.rect = self.image.get_frect(topleft=pos)

        self.get_coin_sound = ResourceManager.load_sound("get_coin.ogg")

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return
        self.kill()
