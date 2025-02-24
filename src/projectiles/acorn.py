from settings import *
from projectiles.projectile import Projectile


class Acorn(Projectile):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(pos, surf, direction, groups)
        self.image = pygame.Surface((8, 8))
        self.gravity = 300
        self.speed = 100
        self.fall = 0
        self.image.fill(color="gray")

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
