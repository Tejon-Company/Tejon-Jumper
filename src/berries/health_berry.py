from berries.berry import Berry
from characters.players.player import Player
from resource_manager import ResourceManager
from singletons.game import Game


class HealthBerry(Berry):
    """
    Implementa una baya que proporciona salud al jugador cuando la recoge.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self._recover_health_sound = ResourceManager.load_sound_effect(
            "recover_health.ogg"
        )
        self._game = Game()

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self._recover_health_sound.play()
        self._game.heal()
        self.kill()
