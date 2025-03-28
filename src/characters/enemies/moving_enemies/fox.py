from characters.enemies.moving_enemies.moving_enemy import MovingEnemy


class Fox(MovingEnemy):
    """
    Implementa a un zorro enemigo que puede moverse de un lado a otro.
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

        self._speed = 75
