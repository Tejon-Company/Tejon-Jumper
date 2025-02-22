from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice


class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="green")

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75
