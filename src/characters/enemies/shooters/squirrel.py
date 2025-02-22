from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.acorn import Acorn


class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, projectile_groups):
        super().__init__(pos, surf, groups, projectile_groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="brown")

        self.rect = self.image.get_frect(topleft=pos)

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            Acorn(
                pos=(self.rect.centerx, self.rect.centery),
                surf=pygame.Surface((8, 8)),
                direction=pygame.math.Vector2(-1, 0),
                groups=self.projectile_groups,
            )
            self.last_shot = current_time
