from characters.utils.check_cooldown import check_cooldown
from characters.utils.normalize_direction import normalize_direction
from characters.utils.collision_utils import *
from characters.utils.animation_utils import *
from characters.character import Character
from resource_manager import ResourceManager
from singletons.game import Game
from singletons.settings.resolution_settings import ResolutionSettings
from pygame.math import Vector2 as vector
import pygame


class Player(Character):
    def __init__(self, pos, surf, groups, level_width):
        super().__init__(pos, surf, groups, None)

        self._setup_animation()
        self.game = Game()
        self.resolution_settings = ResolutionSettings()
        self.level_width = level_width

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.normal_sprite_sheet = ResourceManager.load_sprite_sheet("badger.png")
        self.rage_sprite_sheet = ResourceManager.load_sprite_sheet("rage_badger.png")
        self.current_sprite_sheet = self.normal_sprite_sheet

        self.energy = 100
        self.max_energy = 100
        self.energy_depletion_rate = 30

        self.platform_rects = self.platform_rects

        self.direction = vector(0, 0)
        self.normal_speed = 300
        self.rage_speed = 350
        self.current_speed = self.normal_speed
        self.gravity = 900
        self.fall = 0
        self.is_jumping = False
        self.jump_height = 610
        self.last_time_in_rage = None

        self.on_surface = False
        self.is_sprinting = False
        self.is_in_rage = False

        self.activate_rage_sound = ResourceManager.load_sound_effect(
            "activate_rage.ogg"
        )
        self.deactivate_rage_sound = ResourceManager.load_sound_effect(
            "deactivate_rage.ogg"
        )

    def _setup_animation(self):
        set_animation_parameters(self)

        self.animations = {
            "idle": create_animation_rects(0, 1),
            "run": create_animation_rects(1, 12),
            "jump": create_animation_rects(4, 1),
            "roll": create_animation_rects(13, 8),
        }

        self.current_animation = "idle"
        self.facing_right = True

    def set_platform_rects(self, platform_rects):
        self.platform_rects = platform_rects

    def update(self, delta_time, environment_rects):
        self.old_rect = self.rect.copy()

        self.environment_rects = environment_rects

        self._input()
        self._move(delta_time)
        self._detect_platform_contact()
        self._update_energy(delta_time)
        self._update_animation(delta_time)
        self._update_rage_state()

    def _update_energy(self, delta_time):
        if self.is_in_rage:
            self.recover_energy()

        elif self.is_sprinting and self.energy > 0:
            self.energy -= self.energy_depletion_rate * delta_time
            self.energy = max(0, self.energy)

    def _update_animation(self, delta_time):
        self._determine_current_animation()

        update_animation(delta_time, self, self.animations[self.current_animation])

    def _determine_current_animation(self):
        if self.is_sprinting:
            self.current_animation = "roll"
        elif not self.on_surface:
            self.current_animation = "jump"
        elif abs(self.direction.x) > 0:
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        if self.direction.x != 0:
            self.facing_right = self.direction.x > 0

    def update_sprite(self):
        frame_rect = self.animations[self.current_animation][self.animation_frame]
        self.image = self.current_sprite_sheet.subsurface(frame_rect)

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

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
            keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        )

        self.direction = normalize_direction(self.direction)

    def _move(self, delta_time):
        self._move_horizontally(delta_time)
        self._move_vertically(delta_time)

    def _move_horizontally(self, delta_time):
        sprint_multiplier = 2 if self.is_sprinting else 1
        self.rect.x = self._get_next_pos(delta_time, sprint_multiplier)
        self.handle_collisions_with_rects(self._handle_horizontal_collision)

    def _get_next_pos(self, delta_time, sprint_multiplier):
        next_x_pos = self.rect.x + (
            self.direction.x
            * self._ratio
            * self.current_speed
            * delta_time
            * sprint_multiplier
        )
        left_boundary, right_boundary = self._get_boundaries()

        if next_x_pos > right_boundary:
            next_x_pos = right_boundary
        elif next_x_pos < left_boundary:
            next_x_pos = left_boundary

        return next_x_pos

    def _get_boundaries(self):
        tile_size = self.resolution_settings.tile_size

        left_boundary = 0
        right_boundary = self.level_width * tile_size - tile_size * 2

        return left_boundary, right_boundary

    def _move_vertically(self, delta_time):
        self.rect.y += self.fall * self._ratio * delta_time
        self.fall += self.gravity * delta_time
        self.handle_collisions_with_rects(self._handle_vertical_collision)

        if self.on_surface:
            self.fall = -self.jump_height if self.is_jumping else 0
            self.direction.y = 0

        if self.is_jumping:
            self.direction = normalize_direction(self.direction)
            self.is_jumping = False

        if self.rect.bottom > self.resolution_settings.window_height:
            self.game.handle_dead()

    def handle_collisions_with_rects(self, collision_handler=None):
        for rect in self.platform_rects + self.environment_rects:
            if not rect.colliderect(self.rect):
                continue

            if collision_handler:
                collision_handler(rect)
            else:
                self._handle_vertical_collision(rect)
                self._handle_horizontal_collision(rect)

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
            self.rect, self.platform_rects, self.environment_rects
        )

    def recover_energy(self):
        self.energy = self.max_energy

    def activate_rage(self):
        self.activate_rage_sound.play()
        self.is_in_rage = True
        self.current_sprite_sheet = self.rage_sprite_sheet
        self.current_speed = self.rage_speed

    def _update_rage_state(self):
        if not self.is_in_rage:
            return

        if self.last_time_in_rage is None:
            self.last_time_in_rage = pygame.time.get_ticks()

        rage_elapsed = pygame.time.get_ticks() - self.last_time_in_rage
        has_rage_finished = rage_elapsed >= 10000

        if self.is_in_rage and has_rage_finished:
            self._deactivate_rage()

    def _deactivate_rage(self):
        self.deactivate_rage_sound.play()
        self.is_in_rage = False
        self.current_sprite_sheet = self.normal_sprite_sheet
        self.current_speed = self.normal_speed
