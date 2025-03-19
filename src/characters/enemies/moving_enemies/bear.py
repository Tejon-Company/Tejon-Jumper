from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from characters.players.collision_utils import *
from characters.animation_utils import setup_animation, update_animation
from pygame.sprite import collide_rect


class Bear(MovingEnemy):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, player,
                         platform_rects, sprite_sheet_name, animations, game)

        self.rect = self.image.get_frect(topleft=pos)
        self.rect.width *= 2

        self.direction = vector(-1, 1)
        self.speed = 100
        self.gravity = 1000
        self.fall = 0
        self.is_jumping = False
        self.jump_height = 300
        self.on_surface = True

        self.facing_right = True

        self.remaining_lives = 3
        self.last_damage_time_ms = None

        setup_animation(self)

    def update(self, delta_time, environment_rects):
        self.environment_rects = environment_rects

        self._move(delta_time)
        self._detect_platform_contact()
        update_animation(delta_time, self)
        self._handle_collision_with_player()

    def _handle_collision_with_player(self):
        if not collide_rect(self, self.player):
            return

        self._adjust_player_position()

        is_player_colliding_from_above = is_below_collision(
            self.player.rect, self.player.old_rect, self.rect)

        if is_player_colliding_from_above:
            self._defeat()
            return

        self.game.receive_damage()

    def _move(self, delta_time):
        self._move_horizontally(delta_time)
        self._move_vertically(delta_time)

    def _move_horizontally(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision(self._handle_horizontal_collision)

        if self._will_hit_wall():
            self.direction.x *= -1

        self.facing_right = self.direction.x > 0

    def _will_hit_wall(self):
        wall_height = self.rect.height * 0.6
        wall_offset = (self.rect.height - wall_height) / 2

        wall_rect_right = pygame.FRect(
            (self.rect.right, self.rect.top + wall_offset), (2, wall_height)
        )
        wall_rect_left = pygame.FRect(
            (self.rect.left - 2, self.rect.top + wall_offset), (2, wall_height)
        )

        hit_wall_right = (
            self.direction.x > 0 and (
                wall_rect_right.collidelist(self.platform_rects) >= 0 or
                wall_rect_right.collidelist(self.environment_rects) >= 0
            )
        )
        hit_wall_left = (
            self.direction.x < 0 and (
                wall_rect_left.collidelist(self.platform_rects) >= 0 or
                wall_rect_left.collidelist(self.environment_rects) >= 0
            )
        )
        return hit_wall_right or hit_wall_left

    def _move_vertically(self, delta_time):
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
        self.collision(self._handle_vertical_collision)

        if self.on_surface:
            self.fall = -self.jump_height if self.is_jumping else 0
            self.direction.y = 0

        if self.is_jumping:
            self._normalize_direction()

    def _normalize_direction(self):
        x, y = self.direction
        diagonal_value = .707107

        is_moving_horizontally = (x == 1 or x == -1)
        is_moving_upward = (y == -1 or y == -diagonal_value)

        if is_moving_horizontally and is_moving_upward:
            self.direction.x *= diagonal_value
            if y == -1:
                self.direction.y = -diagonal_value

    def collision(self, collision_handler=None):
        collision_handler = collision_handler or self._handle_horizontal_collision
        for platform_rect in self.platform_rects:
            if not platform_rect.colliderect(self.rect):
                continue

            if collision_handler:
                collision_handler(platform_rect)
            else:
                self._handle_horizontal_collision(platform_rect)
                self._handle_vertical_collision(platform_rect)

        for environment_rect in self.environment_rects:
            if environment_rect.colliderect(self.rect):
                collision_handler(environment_rect)

    def _handle_horizontal_collision(self, platform_rect):
        if is_right_collision(self.rect, self.old_rect, platform_rect):
            self.rect.right = platform_rect.left + TILE_SIZE
            print("right")

        if is_left_collision(self.rect, self.old_rect, platform_rect):
            print("left")

            self.rect.left = platform_rect.right - TILE_SIZE

    def _handle_vertical_collision(self, platform_rect):
        if is_below_collision(self.rect, self.old_rect, platform_rect):
            print("below")
            self.rect.bottom = platform_rect.top

        if is_above_collision(self.rect, self.old_rect, platform_rect):
            print("above")

            self.rect.top = platform_rect.bottom
        self.fall = 0

        self.direction.y = 0

    def _defeat(self):
        if self.remaining_lives <= 0:
            return super()._defeat()

        self.is_jumping = True
        should_receive_damage, self.last_damage_time_ms = check_cooldown(
            self.last_damage_time_ms)

        if should_receive_damage:
            self.remaining_lives -= 1
            self.speed += self.speed * .2

    def _detect_platform_contact(self):
        self.on_surface = is_on_surface(
            self.rect, self.platform_rects, self.environment_rects)
