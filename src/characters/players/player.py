from settings import *
from characters.character import Character
from characters.players.player_state import PlayerState

from resource_manager import ResourceManager


class Player(Character):
    def __init__(self, pos, surf, groups, health_points):
        super().__init__(pos, surf, groups)

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.health_points = health_points
        self.maximum_health_points = health_points

        self.direction = vector(0, 0)
        self.speed = 150
        self.gravity = 1000
        self.fall = 0
        self.jump = False
        self.jump_height = 300

        self.on_surface = False

        self.last_damage_time_ms = None
        self.last_health_time_ms = None

        self.recover_health_sound = ResourceManager.load_sound("recover_health.ogg")

    def receive_damage(self):
        should_receive_damage, self.last_damage_time_ms = Player._check_cooldown(
            self.last_damage_time_ms)

        if not should_receive_damage:
            return PlayerState.ALIVE

        self.health_points -= 1

        if self.health_points > 0:
            return PlayerState.DAMAGED

        return PlayerState.DEAD

    def heal(self):
        has_max_health = self.health_points == self.maximum_health_points
        should_receive_heal, self.last_health_time_ms = Player._check_cooldown(
            self.last_health_time_ms)
        if not has_max_health and should_receive_heal:
            self.health_points += 1
            self.recover_health_sound.play()

    def _check_cooldown(last_time_ms):
        current_time_ms = pygame.time.get_ticks()

        if not last_time_ms:
            return True, current_time_ms

        if current_time_ms < last_time_ms + 2000:
            return False, last_time_ms

        return True, current_time_ms

    def update(self, platform_rects, delta_time):
        self.old_rect = self.rect.copy()
        self._input()
        self._move(platform_rects, delta_time)
        self._detect_platform_contact(platform_rects)

    def _input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.jump = True

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

    def _move(self, platform_rects, delta_time):
        self._move_horizontally(platform_rects, delta_time)
        self._move_vertically(platform_rects, delta_time)

    def _move_horizontally(self, platform_rects, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self._collision(platform_rects, self._handle_horizontal_collision)

    def _move_vertically(self, platform_rects, delta_time):
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
        self._collision(platform_rects, self._handle_vertical_collision)

        if self.on_surface:
            self.fall = -self.jump_height if self.jump else 0
            self.direction.y = 0

        if self.jump:
            self._normalize_direction()
            self.jump = False

    def _collision(self, platform_rects, collision_handler):
        for platform_rect in platform_rects:
            if platform_rect.colliderect(self.rect):
                collision_handler(platform_rect)

    def _handle_horizontal_collision(self, platform_rect):
        self._handle_right_collission(platform_rect)
        self._handle_left_collision(platform_rect)

    def _handle_right_collission(self, platform_rect):
        approaching_from_left = self.rect.right >= platform_rect.left
        player_was_on_left = self.old_rect.right <= platform_rect.left
        is_right_collision = approaching_from_left and player_was_on_left

        if is_right_collision:
            self.rect.right = platform_rect.left

    def _handle_left_collision(self, platform_rect):
        approaching_from_right = self.rect.left <= platform_rect.right
        player_was_on_right = self.old_rect.left >= platform_rect.right
        is_left_collision = approaching_from_right and player_was_on_right

        if is_left_collision:
            self.rect.left = platform_rect.right

    def _handle_vertical_collision(self, platform_rect):
        self._handle_bottom_collision(platform_rect)
        self._handle_top_collision(platform_rect)

        self.direction.y = 0

    def _handle_bottom_collision(self, platform_rect):
        approaching_from_top = self.rect.bottom >= platform_rect.top
        was_above = self.old_rect.bottom <= platform_rect.top
        is_bottom_collision = approaching_from_top and was_above

        if is_bottom_collision:
            self.rect.bottom = platform_rect.top

    def _handle_top_collision(self, platform_rect):
        approaching_from_bottom = self.rect.top <= platform_rect.bottom
        was_below = self.old_rect.top >= platform_rect.bottom
        is_top_collision = approaching_from_bottom and was_below

        if is_top_collision:
            self.rect.top = platform_rect.bottom

    def _detect_platform_contact(self, platform_rects):
        character_height = 2
        platform_rect = pygame.Rect(
            self.rect.bottomleft, (self.rect.width, character_height)
        )

        self.on_surface = platform_rect.collidelist(platform_rects) >= 0
