from resource_manager import ResourceManager
from singletons.game import Game
from sprites.berries.berry import Berry
from sprites.characters.players.player import Player


class HealthBerry(Berry):
    """
    Implementa una baya que proporciona salud al jugador cuando la recoge.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.recover_health_sound = ResourceManager.load_sound_effect(
            "recover_health.ogg"
        )
        self.game = Game()

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

        self.recover_health_sound.play()
        self.game.heal()
        self.kill()
