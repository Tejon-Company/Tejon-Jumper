from settings import *
from characters.players.player import Player
from berries.berry import Berry
from resource_manager import ResourceManager


class EnergyBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.get_energy_sound = ResourceManager.load_sound("get_energy.ogg")

    def update(self, game, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self.get_energy_sound.play()
        player.recover_energy()
        self.kill()
