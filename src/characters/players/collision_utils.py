from pygame.rect import Rect
from pygame.time import get_ticks


def is_right_collision(player_rect, player_old_rect, rect):
    approaching_from_left = player_rect.right >= rect.left
    player_was_on_left = player_old_rect.right <= rect.left
    return approaching_from_left and player_was_on_left


def is_left_collision(player_rect, player_old_rect, rect):
    approaching_from_right = player_rect.left <= rect.right
    player_was_on_right = player_old_rect.left >= rect.right
    return approaching_from_right and player_was_on_right


def is_below_collision(player_rect, player_old_rect, rect):
    approaching_from_top = player_rect.bottom >= rect.top
    was_above = player_old_rect.bottom <= rect.top
    return approaching_from_top and was_above


def is_above_collision(player_rect, player_old_rect, rect):
    approaching_from_bottom = player_rect.top <= rect.bottom
    was_below = player_old_rect.top >= rect.bottom
    return approaching_from_bottom and was_below


def is_on_surface(character_rect, platform_rects, environment_rects):
    rect_height = 1
    platform_rect = Rect(character_rect.bottomleft,
                         (character_rect.width, rect_height))

    on_platform = platform_rect.collidelist(platform_rects) >= 0
    on_environment = platform_rect.collidelist(environment_rects) >= 0

    return on_platform or on_environment


def check_cooldown(last_time_ms, cooldown=2000):
    current_time_ms = get_ticks()

    if not last_time_ms:
        return True, current_time_ms

    if current_time_ms < last_time_ms + cooldown:
        return False, last_time_ms

    return True, current_time_ms
