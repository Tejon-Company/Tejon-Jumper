from projectiles.projectile import Projectile
from singletons.settings.resolution_settings import ResolutionSettings


class Acorn(Projectile):
    def __init__(self, pos, surf, direction, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, direction, groups, sprite_sheet_name, animations)
        self.resolution_settings = ResolutionSettings()
        self.rect = self.image.get_frect(topleft=pos)
        self.gravity = 170 * self.ratio
        self.speed = 100 * self.ratio
        self.fall = 0

    def set_facing_right(self, is_facing_right: bool):
        self._is_facing_right = is_facing_right

    def _move(self, delta_time):
        if self._is_facing_right:
            self.rect.x -= self.direction.x * self.speed * delta_time
        else:
            self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.fall * delta_time
        self.fall += (self.gravity / 2 * delta_time) * self.ratio

    def _reset_projectile_if_off_screen(self):
        if self.rect.y > self.resolution_settings.window_height:
            self._deactivate_projectile()

    def _deactivate_projectile(self):
        self.is_activated = False
        self.fall = 0

    def change_position(self, new_pos_x, new_pos_y):
        self.rect.x = new_pos_x
        self.rect.y = new_pos_y
