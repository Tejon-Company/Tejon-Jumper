from pygame.rect import Rect


def is_right_collision(character_rect, character_old_rect, rect):
    """
    Determina si el personaje está colisionando con un objeto desde la derecha.
    Args:
        character_rect: Rectángulo actual del personaje.
        character_old_rect: Rectángulo previo del personaje.
        rect: Rectángulo del objeto con el que se comprueba la colisión.
    Returns:
        bool: True si el personaje está colisionando desde la derecha, False en caso contrario.
    """

    approaching_from_left = character_rect.right >= rect.left
    character_was_on_left = character_old_rect.right <= rect.left
    return approaching_from_left and character_was_on_left


def is_left_collision(character_rect, character_old_rect, rect):
    """
    Comprueba si hay una colisión por el lado izquierdo de un rectángulo.
    Args:
        character_rect: Rectángulo actual del personaje.
        character_old_rect: Rectángulo anterior del personaje.
        rect: Rectángulo con el que se comprueba la colisión.
    Returns:
        bool: True si hay una colisión desde el lado izquierdo, False en caso contrario.
    """

    approaching_from_right = character_rect.left <= rect.right
    character_was_on_right = character_old_rect.left >= rect.right
    return approaching_from_right and character_was_on_right


def is_below_collision(character_rect, character_old_rect, rect):
    """
    Determina si el personaje está colisionando con un objeto desde arriba.
    Args:
        character_rect: Rectángulo actual del personaje.
        character_old_rect: Rectángulo anterior del personaje.
        rect: Rectángulo del objeto con el que se comprueba la colisión.
    Returns:
        bool: True si el personaje está colisionando desde arriba, False en caso contrario.
    """

    approaching_from_top = character_rect.bottom >= rect.top
    was_above = character_old_rect.bottom <= rect.top
    return approaching_from_top and was_above


def is_above_collision(character_rect, character_old_rect, rect):
    """
    Detecta si hubo una colisión desde arriba.
    Args:
        character_rect: Rectángulo actual del personaje.
        character_old_rect: Rectángulo anterior del personaje.
        rect: Rectángulo con el que se comprueba la colisión.
    Returns:
        bool: True si el personaje colisionó con el objeto desde arriba, False en caso contrario.
    """

    approaching_from_bottom = character_rect.top <= rect.bottom
    was_below = character_old_rect.top >= rect.bottom
    return approaching_from_bottom and was_below


def is_on_surface(character_rect, platform_rects, environment_rects):
    """
    Determina si un personaje está sobre una superficie (plataforma o elemento del entorno).
    Args:
        character_rect: Rectángulo que representa al personaje.
        platform_rects: Lista de rectángulos que representan las plataformas.
        environment_rects: Lista de rectángulos que representan elementos del entorno.
    Returns:
        bool: True si el personaje está sobre una superficie, False en caso contrario.
    """

    rect_height = 1
    platform_rect = Rect(character_rect.bottomleft, (character_rect.width, rect_height))

    on_platform = platform_rect.collidelist(platform_rects) >= 0
    on_environment = platform_rect.collidelist(environment_rects) >= 0

    return on_platform or on_environment
