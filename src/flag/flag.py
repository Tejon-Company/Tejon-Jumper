from characters.sprite import Sprite
from characters.players.player import Player


class Flag(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = surf

        self.rect = self.image.get_frect(topleft=pos)

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return
        self.kill()