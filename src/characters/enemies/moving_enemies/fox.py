from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.players.collision_utils import is_below_collision
from pygame.sprite import collide_rect


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups, platform_rects, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, platform_rects, sprite_sheet_name, animations)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

        self._setup_animation()

    def handle_collision_with_player(self, game, player):
        if not collide_rect(self, player):
            return

        self._adjust_player_position(player)
        is_below = is_below_collision(player.rect, player.old_rect, self.rect)

        if not is_below:
            self.defeat()
        else:
            game.receive_damage()
