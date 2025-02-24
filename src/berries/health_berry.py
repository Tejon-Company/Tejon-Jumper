from settings import *
from characters.players.player import Player
from berries.berry import Berry


class HealthBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = pygame.Surface((32, 32))
        self.image.fill("black")

        self.rect = self.image.get_frect(topleft=pos)

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return
        print(player.health_points)
        player.heal()
        print(player.health_points)
        self.kill()
