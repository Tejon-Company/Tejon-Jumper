from settings import *
from projectiles.projectile import Projectile


class Acorn(Projectile):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(pos, surf, direction, groups)
        self.image = pygame.Surface((8, 8))
        self.gravity = 170
        self.speed = 100
        self.fall = 0
        self.image.fill(color="black")

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time

    def _reset_projectile_if_off_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            self.is_activated = False
            self.fall = 0
