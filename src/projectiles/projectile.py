from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite
from pygame.sprite import collide_rect
from resource_manager import ResourceManager
from singletons.game import Game
from characters.utils.animation_utils import update_animation, setup_animation


class Projectile(Sprite, ABC):
    def __init__(
        self, pos, surf, direction, groups, sprite_sheet_name, animations
    ):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.game = Game()
        self.speed = None
        self.is_activated = False
        self.sprite_sheet = ResourceManager.load_sprite_sheet(sprite_sheet_name)
        self.animations = animations
        setup_animation(self)

    def update(self, delta_time, player):
        if not self.is_activated:
            return

        self._reset_projectile_if_off_screen()
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        update_animation(delta_time, self, self.animations)
        self._process_player_collision(player)

    def update_sprite(self):
        frame_rect = self.animations[self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

    def _setup_animation(self):
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0

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

        self.game.receive_damage(
            is_player_colliding_from_left, is_player_colliding_from_right
        )

    @abstractmethod
    def _deactivate_projectile(self):
        pass

    @abstractmethod
    def change_position(self, new_pos_x, new_pos_y):
        pass
