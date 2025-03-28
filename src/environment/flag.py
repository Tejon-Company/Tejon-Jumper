from environment.environment_element import EnvironmentElement


class Flag(EnvironmentElement):
    """
    Implementa una bandera que, cuando el jugador colisiona con ella,
    desencadena la transición al siguiente nivel y se elimina del juego.
    """

    def __init__(self, pos, surf, groups, player, level):
        super().__init__(pos, surf, groups, player)
        self.rect = self.image.get_rect(topleft=pos)
        self._level = level

    def update(self):
        expanded_rect = self.rect.inflate(2, 2)
        is_colliding = expanded_rect.colliderect(self._player.rect)

        if is_colliding:
            self._level.go_to_next_level()
            self.kill()
