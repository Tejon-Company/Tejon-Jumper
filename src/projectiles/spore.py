from settings import *
from projectiles.projectile import Projectile


class Spore(Projectile):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(pos, surf, direction, groups)
        self.image = pygame.Surface((8, 8))
        self.image.fill(color="yellow")
        self.speed = 70

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time

    def _check_out_of_bounds(self):
        boundary = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        if not self.rect.colliderect(boundary):
            self.is_activated = False
