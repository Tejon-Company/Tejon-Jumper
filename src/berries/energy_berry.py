import pygame

from berries.berry import Berry
from characters.players.player import Player
from resource_manager import ResourceManager


class EnergyBerry(Berry):
    """
    Implementa una baya que al ser recogida por el jugador le permite
    recuperar energía. La baya desaparece temporalmente después de ser
    recogida y reaparece después de un tiempo determinado.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self._original_pos = pygame.Vector2(pos)
        self._respawn_time = None
        self._hidden = False
        self._respawn_duration = 20000
        self._get_energy_sound = ResourceManager.load_sound_effect("get_energy.ogg")

    def update(self, player: Player):
        self._update_visibility_status()
        self._check_collision_with_player(player)

    def _update_visibility_status(self):
        if not self._hidden or pygame.time.get_ticks() < self._respawn_time:
            return

        self._hidden = False
        self._respawn_time = None
        self.rect.topleft = self._original_pos

    def _check_collision_with_player(self, player: Player):
        if not self._hidden and self.rect.colliderect(player.rect):
            player.recover_energy()
            self._get_energy_sound.play()
            self._hide()

    def _hide(self):
        self._hidden = True
        self._respawn_time = pygame.time.get_ticks() + self._respawn_duration
        self.rect.topleft = (-100, -100)

    def draw(self, surface):
        if not self._hidden:
            surface.blit(self.image, self.rect)
