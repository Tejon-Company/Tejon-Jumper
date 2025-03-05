from settings import *
from projectiles.projectile import Projectile


class Spore(Projectile):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(pos, surf, direction, groups)
        self.image = pygame.Surface((8, 8))
        self.image.fill(color="yellow")
        self.speed = 70
        self.initial_pos = 0

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time

    def _reset_projectile_if_off_screen(self):
        if self.rect.x > WINDOW_WIDTH:
            self.is_activated = False