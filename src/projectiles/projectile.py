from settings import *
from abc import ABC, abstractmethod
from characters.sprite import Sprite


class Projectile(Sprite, ABC):
    def __init__(self, pos, surf, direction, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups)
        self.direction = direction
        self.speed = None
        self.is_activated = False
        self.animations = animations
        self._setup_animation()

    def update(self, delta_time):
        if not self.is_activated:
            return
        self._reset_projectile_if_off_screen()
        self.old_rect = self.rect.copy()
        self._move(delta_time)
        self._update_animation(delta_time)

    def _update_animation(self, delta_time):
        self._update_animation_frame(delta_time)
        self._update_sprite()

    def _update_animation_frame(self, delta_time):
        self.animation_time += delta_time
        frames_in_animation = len(self.animations)
        elapsed_frames = self.animation_time / self.animation_speed
        self.animation_frame = int(elapsed_frames) % frames_in_animation

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
    def change_position(self, new_pos_x, new_pos_y):
        pass

    @abstractmethod
    def _move(self, delta_time):
        pass

    @abstractmethod
    def _reset_projectile_if_off_screen(self):
        pass
