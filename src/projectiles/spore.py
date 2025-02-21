from settings import *
from projectiles.projectile import Projectile


class Spore(Projectile):
    def __init__(self, pos, surf, direction, delta_time, speed, groups):
        super().__init__(pos, surf, direction, delta_time, speed, groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time