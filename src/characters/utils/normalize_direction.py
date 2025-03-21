from settings import vector


def normalize_direction(direction):
    x, y = direction
    diagonal_value = 0.707107

    is_moving_horizontally = (x == 1 or x == -1)
    is_moving_upward = (y == -1 or y == -diagonal_value)

    if is_moving_horizontally and is_moving_upward:
        new_x = x * diagonal_value
        new_y = -diagonal_value if y == -1 else y
        return vector(new_x, new_y)

    return direction
