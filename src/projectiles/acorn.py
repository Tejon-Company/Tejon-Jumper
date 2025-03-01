from settings import *
from projectiles.projectile import Projectile


class Acorn(Projectile):
    def __init__(self, pos, surf, direction, groups, camera_x):
        super().__init__(pos, surf, direction, groups, camera_x)
        self.image = pygame.Surface((8, 8))
        self.gravity = 170
        self.speed = 100
        self.fall = 0
        self.image.fill(color="black")

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time

    def _check_out_of_bounds(self):
        boundary = pygame.Rect(-self.camera_x, 0, WINDOW_WIDTH-self.camera_x, WINDOW_HEIGHT)
        if not self.rect.colliderect(boundary):
            self.is_activated = False
            self.fall = 0
