from characters.players.player import Player
from berries.berry import Berry
from resource_manager import ResourceManager
import pygame


class EnergyBerry(Berry):
    """
    Implementa una baya que al ser recogida por el jugador le permite
    recuperar energía. La baya desaparece temporalmente después de ser
    recogida y reaparece después de un tiempo determinado.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.original_pos = pygame.Vector2(pos)
        self.respawn_time = None
        self.hidden = False
        self.respawn_duration = 20000
        self.get_energy_sound = ResourceManager.load_sound_effect("get_energy.ogg")

    def update(self, player: Player):
        self._update_visibility_status()
        self._check_collision_with_player(player)

    def _update_visibility_status(self):
        if not self.hidden or pygame.time.get_ticks() < self.respawn_time:
            return

        self.hidden = False
        self.respawn_time = None
        self.rect.topleft = self.original_pos

    def _check_collision_with_player(self, player: Player):
        if not self.hidden and self.rect.colliderect(player.rect):
            player.recover_energy()
            self.get_energy_sound.play()
            self._hide()

    def _hide(self):
        self.hidden = True
        self.respawn_time = pygame.time.get_ticks() + self.respawn_duration
        self.rect.topleft = (-100, -100)

    def draw(self, surface):
        if not self.hidden:
            surface.blit(self.image, self.rect)
