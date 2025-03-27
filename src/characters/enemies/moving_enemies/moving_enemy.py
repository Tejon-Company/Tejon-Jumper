from characters.enemies.enemy import Enemy
from abc import ABC
from characters.utils.collision_utils import is_on_surface
from characters.utils.animation_utils import set_animation_parameters, update_animation
from random import choice
from pygame.math import Vector2 as vector
import pygame


class MovingEnemy(Enemy, ABC):
    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        platform_rects,
        sprite_sheet_name,
        animations,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            platform_rects,
            sprite_sheet_name,
            animations,
        )

        direction_x = choice((-1, 1))
        self.direction = vector(direction_x, 0)
        self.facing_right = self.direction.x > 0

        set_animation_parameters(self)

    def update(self, delta_time, environment_rects):
        super().update(delta_time)

        update_animation(delta_time, self, self.animations)

        self.old_rect = self.rect.copy()
        self.environment_rects = environment_rects
        self._move(delta_time)
        self._detect_platform_contact()

        self.facing_right = self.direction.x > 0

    def update_sprite(self):
        frame_rect = self.animations[self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.ratio * self.speed * delta_time
        should_change_direction = self._about_to_fall() or self._will_hit_wall()

        if should_change_direction:
            self.direction.x *= -1

    def _about_to_fall(self):
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))

        def check_floor_collision(rect):
            return rect.collidelist(self.platform_rects) < 0

        about_to_fall_right = self.direction.x > 0 and check_floor_collision(
            floor_rect_right
        )
        about_to_fall_left = self.direction.x < 0 and check_floor_collision(
            floor_rect_left
        )

        return about_to_fall_right or about_to_fall_left

    def _will_hit_wall(self):
        wall_height = self.rect.height * 0.6
        wall_offset = (self.rect.height - wall_height) / 2

        wall_rect_right = pygame.FRect(
            (self.rect.right, self.rect.top + wall_offset), (2, wall_height)
        )
        wall_rect_left = pygame.FRect(
            (self.rect.left - 2, self.rect.top + wall_offset), (2, wall_height)
        )

        hit_wall_right = self.direction.x > 0 and (
            wall_rect_right.collidelist(self.platform_rects) >= 0
            or wall_rect_right.collidelist(self.environment_rects) >= 0
        )
        hit_wall_left = self.direction.x < 0 and (
            wall_rect_left.collidelist(self.platform_rects) >= 0
            or wall_rect_left.collidelist(self.environment_rects) >= 0
        )

        return hit_wall_right or hit_wall_left

    def _detect_platform_contact(self):
        self.on_surface = is_on_surface(
            self.rect, self.platform_rects, self.environment_rects
        )
