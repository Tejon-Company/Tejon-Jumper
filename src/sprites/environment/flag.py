from sprites.environment.environment_element import EnvironmentElement


class Flag(EnvironmentElement):
    def __init__(self, pos, surf, groups, player, level):
        super().__init__(pos, surf, groups, player)
        self.rect = self.image.get_rect(topleft=pos)
        self.level = level

    def update(self):
        is_colliding = self.rect.colliderect(self.player.rect)

        if is_colliding:
            self.level.go_to_next_level()
            self.kill()
