from environment.environment_element import EnvironmentElement


class Flag(EnvironmentElement):
    def __init__(self, pos, surf, groups, player, game):
        super().__init__(pos, surf, groups, player)
        self.rect = self.image.get_rect(topleft=pos)
        self.game = game

    def update(self):
        expanded_rect = self.rect.inflate(1, 1)
        is_colliding = expanded_rect.colliderect(self.player.rect)

        if is_colliding:
            self.game.next_level()
            self.kill()
