from settings import *
from projectiles.projectile import Projectile


class Spore(Projectile):
    def __init__(self, pos, surf, direction, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, direction, groups, sprite_sheet_name, animations)
        self.image = pygame.Surface((8, 8))
        self.image.fill(color="yellow")
        self.speed = 70
        self.max_distance = 200

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time

    def _reset_projectile_if_off_screen(self):
        if self._is_projectile_off_screen():
            self._deactivate_projectile()

    def _is_projectile_off_screen(self):
        distance_traveled = self._calculate_travel_distance()
        return self._check_position_exceeds_distance(distance_traveled)

    def _calculate_travel_distance(self):
        if self.direction.x > 0:
            return self.initial_x_pos + self.max_distance
        return self.initial_x_pos - self.max_distance

    def _check_position_exceeds_distance(self, distance_traveled):
        if self.direction.x > 0:
            return self.rect.x >= distance_traveled
        return self.rect.x <= distance_traveled

    def _deactivate_projectile(self):
        self.is_activated = False
        self.rect.x = -100
        self.rect.y = -100

    def change_position(self, new_pos_x, new_pos_y):
        self.rect.x = new_pos_x
        self.rect.y = new_pos_y
        self.initial_x_pos = new_pos_x
