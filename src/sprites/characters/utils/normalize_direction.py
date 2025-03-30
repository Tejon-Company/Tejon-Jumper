from pygame.math import Vector2 as vector


def normalize_direction(direction):
    """
    Normaliza el vector de dirección para movimientos diagonales hacia
    arriba. Args:
        direction: Un par ordenado (x, y) que representa la dirección de
        movimiento.
            donde x representa el movimiento horizontal (-1: izquierda,
            1: derecha) y donde y representa el movimiento vertical (-1:
            arriba, 1: abajo)
    Returns:
        La dirección normalizada. Si el movimiento es diagonal hacia
        arriba, se ajustan los componentes para mantener un vector
        unitario (aproximadamente 0.707 en cada componente). En otro
        caso, se devuelve la dirección original.
    """

    x, y = direction
    diagonal_value = 0.707107

    is_moving_horizontally = x == 1 or x == -1
    is_moving_upward = y == -1 or y == -diagonal_value

    if is_moving_horizontally and is_moving_upward:
        new_x = x * diagonal_value
        new_y = -diagonal_value if y == -1 else y
        return vector(new_x, new_y)

    return direction
