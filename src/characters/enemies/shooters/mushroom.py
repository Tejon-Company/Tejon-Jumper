from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.spore import Spore


class Mushroom(Shooter):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="pink")

        self.rect = self.image.get_frect(topleft=pos)

    def _shoot(self, delta_time):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            Spore(
                pos=(self.rect.centerx, self.rect.centery),
                surf=pygame.Surface((8, 8)),
                direction=pygame.math.Vector2(-1, 0),
                delta_time=delta_time,
                speed=5,
                groups=[self.projectiles]
            )
            self.last_shot = current_time
