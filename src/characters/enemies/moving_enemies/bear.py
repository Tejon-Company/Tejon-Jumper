from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from characters.players.collision_utils import check_cooldown, is_below_collision
from characters.animation_utils import setup_animation
from pygame.sprite import collide_rect


class Bear(MovingEnemy):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, player,
                         platform_rects, sprite_sheet_name, animations, game)

        self.rect = self.image.get_frect(topleft=pos)
        self.rect.width *= 2

        self.direction = -1
        self.speed = 100

        self.remaining_lives = 3
        self.last_damage_time_ms = None

        setup_animation(self)

    def _handle_collision_with_player(self):
        if not collide_rect(self, self.player):
            return

        self._adjust_player_position()

        is_player_colliding_from_above = is_below_collision(
            self.player.rect, self.player.old_rect, self.rect)

        if is_player_colliding_from_above:
            self._defeat()
            return

        self.game.receive_damage()

    def _defeat(self):
        if self.remaining_lives <= 0:
            return super()._defeat()

        should_receive_damage, self.last_damage_time_ms = check_cooldown(
            self.last_damage_time_ms)

        if should_receive_damage:
            self.remaining_lives -= 1
            self.speed += self.speed * .2
