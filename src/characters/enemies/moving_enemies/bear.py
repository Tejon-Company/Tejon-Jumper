from characters.utils.check_cooldown import check_cooldown
from characters.utils.normalize_direction import normalize_direction
from characters.utils.collision_utils import is_below_collision
from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from characters.utils.animation_utils import setup_animation, update_animation
from pygame.sprite import collide_rect


class Bear(MovingEnemy):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, player,
                         platform_rects, sprite_sheet_name, animations, game)

        self.rect = self.image.get_frect(topleft=pos)
        self.rect.width = TILE_SIZE * 2

        self.direction = vector(-1, 1)
        self.speed = 100
        self.gravity = 1000
        self.fall = 0
        self.is_jumping = False
        self.jump_height = 250

        self.on_surface = True

        self.facing_right = True

        self.health_points = 3
        self.last_damage_time_ms = None

        setup_animation(self)

    def update(self, delta_time, environment_rects):
        self.environment_rects = environment_rects

        self._move(delta_time)
        self._detect_platform_contact()
        update_animation(delta_time, self)
        self._handle_collision_with_player()

    def _move(self, delta_time):
        self._move_horizontally(delta_time)
        self._move_vertically(delta_time)

    def _move_horizontally(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time

        if self._will_hit_wall(self.direction.x):
            self.direction.x *= -1

        self.facing_right = self.direction.x > 0

    def _move_vertically(self, delta_time):
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
        self._handle_collisions_with_rects()

        if self.on_surface:
            self.fall = -self.jump_height if self.is_jumping else 0
            self.direction.y = 0

        if self.is_jumping:
            self.direction = normalize_direction(self.direction)

    def _handle_collisions_with_rects(self):
        for rect in self.platform_rects + self.environment_rects:
            if rect.colliderect(self.rect):
                self._handle_vertical_collision(rect)

    def _handle_vertical_collision(self, platform_rect):
        if is_below_collision(self.rect, self.old_rect, platform_rect):
            self.rect.bottom = platform_rect.top

        self.fall = 0
        self.direction.y = 0

    def _handle_collision_with_player(self):
        if not collide_rect(self, self.player):
            return

        self._adjust_player_position()

        is_player_colliding_from_above = self._is_collision_from_above()

        if is_player_colliding_from_above:
            self._receive_damage()
            return

        should_damage, _ = check_cooldown(self.last_damage_time_ms)
        if should_damage:
            is_player_colliding_from_left = self.player.rect.centerx > self.rect.centerx
            is_player_colliding_from_right = self.player.rect.centerx < self.rect.centerx

            self.game.receive_damage(
                is_player_colliding_from_left, is_player_colliding_from_right)

    def _is_collision_from_above(self):
        approaching_from_top = self.player.rect.bottom >= self.rect.top
        was_above = self.player.old_rect.bottom <= self.old_rect.top
        return approaching_from_top and was_above

    def _receive_damage(self):
        if self.health_points <= 0:
            return self._defeat()

        self.is_jumping = True
        should_receive_damage, self.last_damage_time_ms = check_cooldown(
            self.last_damage_time_ms)

        if should_receive_damage:
            self.health_points -= 1
            self.speed += self.speed * .2
