from settings import *
from characters.character import Character
from characters.players.collision_utils import *


class Player(Character):
    def __init__(self, pos, surf, groups, health_points, sprite_sheet_name):
        super().__init__(pos, surf, groups, None, sprite_sheet_name)

        self._setup_animation()

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.health_points = health_points
        self.maximum_health_points = health_points

        self.energy = 100
        self.max_energy = 100
        self.energy_depletion_rate = 30

        self.platform_rects = self.platform_rects

        self.direction = vector(0, 0)
        self.speed = 150
        self.gravity = 1000
        self.fall = 0
        self.is_jumping = False
        self.jump_height = 300

        self.on_surface = False
        self.is_sprinting = False

        self.last_health_time_ms = None

    def _setup_animation(self):
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0

        self.animations = {
            'idle': [(0, 0, 32, 32)],
            'run': [(x + (x//32), 0, 32, 32) for x in range(64, 416, 32)],
            'jump': [(165, 0, 32, 32)],
            'roll': [(x, 0, 32, 32) for x in range(429, 640, 32)],
        }

        self.current_animation = 'idle'
        self.facing_right = True

    def set_platform_rects(self, platform_rects):
        self.platform_rects = platform_rects

    def heal(self):
        has_max_health = self.health_points == self.maximum_health_points
        should_receive_heal, self.last_health_time_ms = Player._check_cooldown(
            self.last_health_time_ms)

        if not has_max_health and should_receive_heal:
            self.health_points += 1

    def _check_cooldown(last_time_ms):
        current_time_ms = pygame.time.get_ticks()

        if not last_time_ms:
            return True, current_time_ms

        if current_time_ms < last_time_ms + 2000:
            return False, last_time_ms

        return True, current_time_ms

    def update(self, delta_time, environment_rects):
        self.platform_rects = self.platform_rects
        self.old_rect = self.rect.copy()

        self.environment_rects = environment_rects

        self._input()
        self._move(delta_time)
        self._detect_platform_contact()
        self._update_energy(delta_time)
        self._update_animation(delta_time)

    def _update_energy(self, delta_time):
        if self.is_sprinting and self.energy > 0:
            self.energy -= self.energy_depletion_rate * delta_time
            self.energy = max(0, self.energy)

    def _update_animation(self, delta_time):
        previous_animation = self.current_animation
        self._determine_current_animation()

        if previous_animation != self.current_animation:
            self._reset_animation()

        self._update_animation_frame(delta_time)
        self._update_sprite()

    def _determine_current_animation(self):
        if self.is_sprinting:
            self.current_animation = 'roll'
        elif not self.on_surface:
            self.current_animation = 'jump'
        elif abs(self.direction.x) > 0:
            self.current_animation = 'run'
        else:
            self.current_animation = 'idle'

        self.facing_right = self.direction.x > 0

    def _reset_animation(self):
        self.animation_time = 0
        self.animation_frame = 0

    def _update_animation_frame(self, delta_time):
        self.animation_time += delta_time
        frames_in_animation = len(self.animations[self.current_animation])
        elapsed_frames = self.animation_time / self.animation_speed
        self.animation_frame = int(elapsed_frames) % frames_in_animation

    def _update_sprite(self):
        frame_rect = self.animations[self.current_animation][self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

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
            self.is_jumping = True

        self.is_sprinting = self.energy > 0 and (
            keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])

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

    def _move(self, delta_time):
        self._move_horizontally(delta_time)
        self._move_vertically(delta_time)

    def _move_horizontally(self, delta_time):
        sprint_multiplier = 2 if self.is_sprinting else 1
        self.rect.x += self.direction.x * self.speed * delta_time * sprint_multiplier
        self.collision(self._handle_horizontal_collision)

    def _move_vertically(self, delta_time):
        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
        self.collision(self._handle_vertical_collision)

        if self.on_surface:
            self.fall = -self.jump_height if self.is_jumping else 0
            self.direction.y = 0

        if self.is_jumping:
            self._normalize_direction()
            self.is_jumping = False

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
            self.rect.right = platform_rect.left

        if is_left_collision(self.rect, self.old_rect, platform_rect):
            self.rect.left = platform_rect.right

    def _handle_vertical_collision(self, platform_rect):
        if is_below_collision(self.rect, self.old_rect, platform_rect):
            self.rect.bottom = platform_rect.top

        if is_above_collision(self.rect, self.old_rect, platform_rect):
            self.rect.top = platform_rect.bottom
        self.fall = 0

        self.direction.y = 0

    def _detect_platform_contact(self):
        self.on_surface = is_on_surface(
            self.rect, self.platform_rects, self.environment_rects)

    def recover_energy(self):
        self.energy = self.max_energy
