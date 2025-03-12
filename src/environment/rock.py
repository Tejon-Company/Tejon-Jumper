from environment.environment_element import EnvironmentElement
from characters.players.player import Player


class Rock(EnvironmentElement):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, player: Player):
        expanded_rect = self.rect.inflate(1,1)
        is_side_colliding = expanded_rect.colliderect(player.rect)
        print(
            f"is sprinting = {player.is_sprinting}     colliding={is_side_colliding}")

        if player.is_sprinting and is_side_colliding:
            self.kill()
