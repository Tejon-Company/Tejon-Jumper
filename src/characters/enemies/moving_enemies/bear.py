from characters.enemies.moving_enemies.moving_enemy import MovingEnemy


class Bear(MovingEnemy):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, player,
                         platform_rects, sprite_sheet_name, animations, game)

        self.rect = self.image.get_frect(topleft=pos)
        self.rect.width *= 2
        print("Bear rect dimensions:", self.rect.width, "x", self.rect.height)

        self.direction = -1
        self.speed = 100

        self._setup_animation()
