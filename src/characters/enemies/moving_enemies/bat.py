from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from characters.players.player_state import PlayerState
from characters.enemies.enemy_collision_directions import CollisionDirection

class Bat(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = pygame.Surface((32, 32))
        self.image.fill("black")

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

    
    def handle_collision_with_player(self, level, player):
        player_state = None
        direction = self.get_collision_direction(player)  # Esto devuelve un CollisionDirection Enum
        super().adjust_player_position(player)

        if player.is_sprinting or direction == CollisionDirection.BELOW:
            self.defeat()
        elif direction in [CollisionDirection.LEFT, CollisionDirection.RIGHT, CollisionDirection.ABOVE]:
            player_state = player.receive_damage()
            if player_state == PlayerState.DEAD:
                level.handle_dead()
                
