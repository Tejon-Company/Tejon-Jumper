from environment.environment_element import EnvironmentElement


class Rock(EnvironmentElement):
    """
    Maneja las interacciones entre las rocas y el jugador.
    Las rocas se pueden destruir cuando el jugador está corriendo y colisiona con ellas.
    """

    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups, player)

    def update(self):
        expanded_rect = self.rect.inflate(1, 1)
        is_colliding = expanded_rect.colliderect(self.player.rect)

        if self.player.is_sprinting and is_colliding:
            self.kill()
