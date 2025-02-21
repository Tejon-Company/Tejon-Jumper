from settings import *
from src.characters.enemies.enemy import Enemy


class Shooter(Enemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.shoot_cooldown = 2000
        self.last_shot = 0
        self.projectiles = pygame.sprite.Group()

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            projectile = Projectile(
                pos=(self.rect.centerx, self.rect.centery),
                direction=pygame.math.Vector2(-1, 0),
                speed=5,
                groups=[self.projectiles]
            )
            self.last_shot = current_time

    def update(self):
        super().update()
        self._shoot()
        self.projectiles.update()
