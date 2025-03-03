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
        if self.is_activated:
            self.rect.x += self.direction.x * self.speed * delta_time

    def _reset_projectile_if_off_screen(self):
        traveled_distance = abs(self.rect.x - self.initial_pos)
        if traveled_distance > 3 * TILE_SIZE:
            print(f"rect x: {self.rect.x}    Initial position: {self.initial_pos}")
            self.is_activated = False
