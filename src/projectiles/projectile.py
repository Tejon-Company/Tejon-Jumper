from abc import ABC, abstractmethod

from pygame.sprite import collide_rect

from characters.sprite import Sprite
from characters.utils.animation_utils import set_animation_parameters, update_animation
from resource_manager import ResourceManager
from singletons.game import Game
from singletons.settings.resolution_settings import ResolutionSettings


class Projectile(Sprite, ABC):
    """
    Clase abstracta que implementa la funcionalidad básica para los proyectiles que pueden
    interactuar con el jugador. Maneja la activación, movimiento, animación y colisiones
    de los proyectiles.
    """

    def __init__(self, pos, surf, direction, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self._game = Game()
        self._resolution_settings = ResolutionSettings()
        self._ratio = self._resolution_settings.tile_size / 64
        self._speed = None
        self.is_activated = False
        self._sprite_sheet = ResourceManager.load_sprite_sheet(sprite_sheet_name)
        self._animations = animations
        set_animation_parameters(self)

    def update(self, delta_time, player):
        if not self.is_activated:
            return

        self._reset_projectile_if_off_screen()
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        update_animation(delta_time, self, self._animations)
        self._process_player_collision(player)

    def update_sprite(self):
        frame_rect = self._animations[self.animation_frame]
        self.image = self._sprite_sheet.subsurface(frame_rect)

    @abstractmethod
    def _reset_projectile_if_off_screen(self):
        pass

    @abstractmethod
    def _move(self, delta_time):
        pass

    def _process_player_collision(self, player):
        if not collide_rect(self, player):
            return

        self._deactivate_projectile()

        if player.is_in_rage:
            return

        is_player_colliding_from_left = player.rect.centerx > self.rect.centerx
        is_player_colliding_from_right = player.rect.centerx < self.rect.centerx

        self._game.receive_damage(
            is_player_colliding_from_left, is_player_colliding_from_right
        )

    @abstractmethod
    def _deactivate_projectile(self):
        pass

    @abstractmethod
    def change_position(self, new_pos_x, new_pos_y):
        pass
