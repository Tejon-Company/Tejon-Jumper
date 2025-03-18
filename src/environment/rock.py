from environment.environment_element import EnvironmentElement
from characters.players.player import Player


class Rock(EnvironmentElement):
    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups, player)

    def update(self, player: Player):
        expanded_rect = self.rect.inflate(1, 1)
        is_side_colliding = expanded_rect.colliderect(player.rect)
        player.environment_collision(self.rect)
        if player.is_sprinting and is_side_colliding:
            self.kill()
