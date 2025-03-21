from settings import *
from characters.players.player import Player
from berries.berry import Berry


class EnergyBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.original_pos = pygame.Vector2(pos)
        self.respawn_time = None
        self.hidden = False
        self.respawn_duration = 20000

    def update(self, game, player: Player):
        self._check_respawn()
        if self.hidden:
            return
        self._check_collision(player)

    def _check_respawn(self):
        if self.hidden and pygame.time.get_ticks() >= self.respawn_time:
            self._show()

    def _check_collision(self, player: Player):
        if self.rect.colliderect(player.rect):
            player.recover_energy()
            self._hide()

    def _hide(self):
        self.hidden = True
        self.respawn_time = pygame.time.get_ticks() + self.respawn_duration
        self.rect.topleft = (-100, -100)

    def _show(self):
        self.hidden = False
        self.respawn_time = None
        self.rect.topleft = self.original_pos

    def draw(self, surface):
        if not self.hidden:
            surface.blit(self.image, self.rect)
