from settings import *
from entities.character import Character


class Enemy(Character):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def _move(self, platform_group, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

        collision_rects = [sprite.rect for sprite in platform_group]

        self._change_direction_if_falling(collision_rects)

    def _change_direction_if_falling(self, collision_rects):
        if self._should_change_direction(collision_rects):
            self.direction *= -1

    def _should_change_direction(self, collision_rects):
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))

        check_floor_collision = lambda rect: rect.collidelist(collision_rects) < 0

        about_to_fall_right = self.direction > 0 and check_floor_collision(
            floor_rect_right
        )
        about_to_fall_left = self.direction < 0 and check_floor_collision(
            floor_rect_left
        )

        return about_to_fall_right or about_to_fall_left

    def _detect_platform_contact(self, platform_group):
        floor_rect = pygame.Rect(
            self.rect.bottomleft, (self.rect.width, self.rect.height)
        )
        collide_rects = [sprite.rect for sprite in platform_group]

        self.on_surface = floor_rect.collidelist(collide_rects) >= 0
