from settings import *
from characters.players.player import Player
from berries.berry import Berry
from resource_manager import ResourceManager


class HealthBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.recover_health_sound = ResourceManager.load_sound_effect(
            "recover_health.ogg")

    def update(self, game, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self.recover_health_sound.play()
        game.heal()
        self.kill()
