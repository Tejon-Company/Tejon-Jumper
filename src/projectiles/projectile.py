from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite
from characters.utils.collision_utils import is_below_collision
from pygame.sprite import collide_rect
from resource_manager import ResourceManager
from characters.utils.animation_utils import update_animation, setup_animation


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, groups, game, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.game = game
        self.speed = None
        self.is_activated = False
        self.sprite_sheet = ResourceManager.load_sprite_sheet(
            sprite_sheet_name)
        self.animations = animations
        setup_animation(self)

    def update(self, delta_time, player):
        if not self.is_activated:
            return

        self._reset_projectile_if_off_screen()
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        update_animation(delta_time, self)
        self._handle_collision_with_player(player)

    def _update_sprite(self):
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

    def _handle_collision_with_player(self, player):
        if not collide_rect(self, player):
            return

        is_player_colliding_from_above = is_below_collision(
            player.rect, player.old_rect, self.rect)

        if is_player_colliding_from_above or player.is_sprinting:
            self._deactivate_projectile()
            return

        self.game.receive_damage()
        self._deactivate_projectile()

    @abstractmethod
    def _deactivate_projectile(self):
        pass

    @abstractmethod
    def change_position(self, new_pos_x, new_pos_y):
        pass
