from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy


class Bat(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        #self.image = pygame.Surface((32, 32))
        #self.image.fill("black")

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = vector(-1, 1)
        self.x_speed = 50
        self.y_speed = 100

        pos_x, pos_y = pos

        self.top_pos = pos_y
        self.bottom_pos = pos_y + TILE_SIZE * 4

        self.left_limit = pos_x - TILE_SIZE * 4
        self.right_limit = pos_x + TILE_SIZE * 4

    def update(self, platform_rects, delta_time):
        self._move(delta_time)
        self._check_path()

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.x_speed * delta_time
        self.rect.y += self.direction.y * self.y_speed * delta_time

    def _check_path(self):
        above_top_position = self.rect.y < self.top_pos
        below_bottom_position = self.rect.y > self.bottom_pos

        if above_top_position:
            self.direction.x *= -1
            self.direction.y *= -1

        if below_bottom_position:
            self.direction.y = -1
