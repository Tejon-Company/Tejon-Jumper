from pygame.time import get_ticks


def check_cooldown(last_time_ms, cooldown=2000):
    """
    Comprueba si ha pasado el tiempo de espera (cooldown) desde la última activación.
    Args:
        last_time_ms: Timestamp en milisegundos de la última activación.
        cooldown: Tiempo de espera en milisegundos. Por defecto es 2000ms.
    Returns:
        Tupla de (bool, int):
            - bool: True si el cooldown ha terminado o si es la primera activación, False si aún está en espera.
            - int: El timestamp actual si el cooldown ha terminado, o el timestamp anterior si aún está en espera.
    """

    current_time_ms = get_ticks()

    if not last_time_ms:
        return True, current_time_ms

    if current_time_ms < last_time_ms + cooldown:
        return False, last_time_ms

    return True, current_time_ms
