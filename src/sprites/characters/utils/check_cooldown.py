from pygame.time import get_ticks


def check_cooldown(last_time_ms, cooldown=2000):
    current_time_ms = get_ticks()

    if not last_time_ms:
        return True, current_time_ms

    if current_time_ms < last_time_ms + cooldown:
        return False, last_time_ms

    return True, current_time_ms
