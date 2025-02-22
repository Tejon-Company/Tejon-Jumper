from settings import *
from projectiles.projectile import Projectile


class Acorn(Projectile):
    def __init__(self, pos, surf, direction, speed, groups):
        super().__init__(pos, surf, direction, speed, groups)
        self.image = pygame.Surface((8, 8))
        self.image.fill(color="gray")

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time
