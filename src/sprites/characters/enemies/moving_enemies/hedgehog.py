from sprites.characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from sprites.characters.utils.collision_utils import is_below_collision


class Hedgehog(MovingEnemy):
    """
    Implementa a un erizo enemigo que puede moverse de un lado a otro.
    """

    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        platform_rects,
        sprite_sheet_name,
        animations,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            platform_rects,
            sprite_sheet_name,
            animations,
        )

        self.rect = self.image.get_frect(topleft=pos)

        self.speed = 50

    def _check_should_receive_damage(self):
        is_below = is_below_collision(self.player.rect, self.player.old_rect, self.rect)
        self.should_receive_damage = self.player.is_in_rage or (
            self.player.is_sprinting and not is_below
        )
