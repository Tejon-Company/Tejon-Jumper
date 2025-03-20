import pygame
from settings import *
from characters.players.player import Player
from berries.berry import Berry


class EnergyBerry(Berry):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.original_pos = pygame.Vector2(pos)
        self.respawn_time = None
        self.hidden = False

    def update(self, game, player: Player):
        current_time = pygame.time.get_ticks()

        if self.hidden and current_time >= self.respawn_time:
            self.respawn_time = None
            self.hidden = False
            self.rect.topleft = self.original_pos
            return

        if self.hidden:
            return

        if self.rect.colliderect(player.rect):
            player.recover_energy()
            self.respawn_time = current_time + 2000
            self.hidden = True
            self.rect.topleft = (-100, -100)

    def draw(self, surface):
        if not self.hidden:
            surface.blit(self.image, self.rect)
