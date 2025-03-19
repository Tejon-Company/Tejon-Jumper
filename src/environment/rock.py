from environment.environment_element import EnvironmentElement


class Rock(EnvironmentElement):
    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups, player)

    def update(self):
        expanded_rect = self.rect.inflate(1, 1)
        is_colliding = expanded_rect.colliderect(self.player.rect)

        if self.player.is_sprinting and is_colliding:
            self.kill()
