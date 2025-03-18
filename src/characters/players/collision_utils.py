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
