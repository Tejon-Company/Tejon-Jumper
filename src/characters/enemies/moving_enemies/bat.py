from pygame.math import Vector2 as vector

from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from characters.utils.animation_utils import update_animation
from singletons.settings.resolution_settings import ResolutionSettings


class Bat(MovingEnemy):
    """
    Implementa un enemigo murciélago en el juego.
    Se mueve diagonalmente dentro de un área definida por límites superior e inferior,
    y cambia de dirección cuando alcanza dichos límites. El murciélago oscila entre una posición
    superior e inferior establecidas durante su inicialización.
    """

    def __init__(self, pos, surf, groups, player, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, player, None, sprite_sheet_name, animations)

        self._resolution_settings = ResolutionSettings()
        self.rect = self.image.get_frect(topleft=pos)

        self._direction = vector(-1, 1)
        self._x_speed = 50
        self._y_speed = 100

        pos_x, pos_y = pos

        self._top_pos = pos_y
        self._bottom_pos = pos_y + self._resolution_settings.tile_size * 4

        self._left_limit = pos_x - self._resolution_settings.tile_size * 4
        self._right_limit = pos_x + self._resolution_settings.tile_size * 4

    def update(self, delta_time, environment_rects):
        self._check_should_receive_damage()
        self._process_player_collision()

        update_animation(delta_time, self, self._animations)

        self.old_rect = self.rect.copy()

        self._move(delta_time)
        self._check_path()

        self._facing_right = self._direction.x > 0
        update_animation(delta_time, self, self._animations)

    def _move(self, delta_time):
        self.rect.x += self._direction.x * self._ratio * self._x_speed * delta_time
        self.rect.y += self._direction.y * self._ratio * self._y_speed * delta_time

    def _check_path(self):
        above_top_position = self.rect.y < self._top_pos
        below_bottom_position = self.rect.y > self._bottom_pos

        if above_top_position:
            self._direction.x *= -1
            self._direction.y *= -1

        if below_bottom_position:
            self._direction.y = -1
