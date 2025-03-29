from sprites.characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from sprites.characters.utils.animation_utils import update_animation
from singletons.settings.resolution_settings import ResolutionSettings
from pygame.math import Vector2 as vector


class Bat(MovingEnemy):
    def __init__(self, pos, surf, groups, player, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, player, None, sprite_sheet_name, animations)

        self.resolution_settings = ResolutionSettings()
        self.rect = self.image.get_frect(topleft=pos)

        self.direction = vector(-1, 1)
        self.x_speed = 50
        self.y_speed = 100

        pos_x, pos_y = pos

        self.top_pos = pos_y
        self.bottom_pos = pos_y + self.resolution_settings.tile_size * 4

        self.left_limit = pos_x - self.resolution_settings.tile_size * 4
        self.right_limit = pos_x + self.resolution_settings.tile_size * 4

    def update(self, delta_time, environment_rects):
        self._check_should_receive_damage()
        self._process_player_collision()

        update_animation(delta_time, self, self.animations)

        self.old_rect = self.rect.copy()

        self._move(delta_time)
        self._check_path()

        self.facing_right = self.direction.x > 0
        update_animation(delta_time, self, self.animations)

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self._ratio * self.x_speed * delta_time
        self.rect.y += self.direction.y * self._ratio * self.y_speed * delta_time

    def _check_path(self):
        above_top_position = self.rect.y < self.top_pos
        below_bottom_position = self.rect.y > self.bottom_pos

        if above_top_position:
            self.direction.x *= -1
            self.direction.y *= -1

        if below_bottom_position:
            self.direction.y = -1
