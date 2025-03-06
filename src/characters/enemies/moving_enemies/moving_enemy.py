from settings import *
from characters.enemies.enemy import Enemy
from abc import ABC


class MovingEnemy(Enemy, ABC):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, platform_rects, delta_time):
        self.old_rect = self.rect.copy()
        self._move(platform_rects, delta_time)
        self._detect_platform_contact(platform_rects)

    def _move(self, platform_rects, delta_time):
        self.rect.x += self.direction * self.speed * delta_time
        self._change_direction_if_falling(platform_rects)

    def _change_direction_if_falling(self, platform_rects):
        if self._should_change_direction(platform_rects):
            self.direction *= -1

    def _should_change_direction(self, platform_rects):
        return self._about_to_fall(platform_rects) or self._will_hit_wall(
            platform_rects
        )

    def _about_to_fall(self, platform_rects):
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))

        def check_floor_collision(
            rect): return rect.collidelist(platform_rects) < 0

        about_to_fall_right = self.direction > 0 and check_floor_collision(
            floor_rect_right
        )
        about_to_fall_left = self.direction < 0 and check_floor_collision(
            floor_rect_left
        )

        return about_to_fall_right or about_to_fall_left

    def _will_hit_wall(self, platform_rects):
        wall_height = self.rect.height * 0.6
        wall_offset = (self.rect.height - wall_height) / 2

        wall_rect_right = pygame.FRect(
            (self.rect.right, self.rect.top + wall_offset), (2, wall_height)
        )
        wall_rect_left = pygame.FRect(
            (self.rect.left - 2, self.rect.top + wall_offset), (2, wall_height)
        )

        hit_wall_right = (
            self.direction > 0 and wall_rect_right.collidelist(
                platform_rects) >= 0
        )
        hit_wall_left = (
            self.direction < 0 and wall_rect_left.collidelist(
                platform_rects) >= 0
        )

        return hit_wall_right or hit_wall_left

    def _detect_platform_contact(self, platform_rects):
        floor_rect = pygame.Rect(
            self.rect.bottomleft, (self.rect.width, self.rect.height)
        )

        self.on_surface = floor_rect.collidelist(platform_rects) >= 0
    