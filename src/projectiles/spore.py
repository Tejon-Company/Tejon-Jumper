from settings import *
from projectiles.projectile import Projectile


class Spore(Projectile):
    def __init__(self, pos, surf, direction, groups, game):
        super().__init__(pos, surf, direction, groups, game)
        self.image = pygame.Surface((8, 8))
        self.image.fill(color="yellow")
        self.speed = 70
        self.max_distance = 200

    def _move(self, delta_time):
        if self.direction[0] != 0:
            self.rect.x += self.direction.x * self.speed * delta_time
        else:
            self.rect.y += self.direction.y * self.speed * delta_time

    def _reset_projectile_if_off_screen(self):
        if self._is_projectile_off_screen():
            self._deactivate_projectile()

    def _is_projectile_off_screen(self):
        distance_traveled = self._calculate_travel_distance()
        return self._check_position_exceeds_distance(distance_traveled)

    def _calculate_travel_distance(self):
        if self._is_moving_horizontally():
            return self._calculate_distance(self.direction.x, self.initial_x_pos)
        else:
            return self._calculate_distance(self.direction.y, self.initial_y_pos)

    def _calculate_distance(self, direction, initial_pos):
        if direction > 0:
            return initial_pos + self.max_distance
        return initial_pos - self.max_distance

    def _check_position_exceeds_distance(self, distance_traveled):
        if self._is_moving_horizontally():
            return self._check_if_position_exceeded(distance_traveled, self.direction.x, self.rect.x)
        else:
            return self._check_if_position_exceeded(distance_traveled, self.direction.y, self.rect.y)

    def _is_moving_horizontally(self):
        return self.direction.x != 0

    def _check_if_position_exceeded(self, distance_traveled, direction, rect):
        if direction > 0:
            return rect >= distance_traveled
        return rect <= distance_traveled

    def _deactivate_projectile(self):
        self.is_activated = False
        self.rect.x = -100
        self.rect.y = -100

    def change_position(self, new_pos_x, new_pos_y, new_direction=None):
        self.rect.x = new_pos_x
        self.rect.y = new_pos_y
        self.initial_x_pos = new_pos_x
        self.initial_y_pos = new_pos_y

    def change_direction(self, new_direction):
        self.direction = new_direction
