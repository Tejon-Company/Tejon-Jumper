import pygame

from singletons.settings.difficulty_settings import DifficultySettings
from singletons.settings.resolution_settings import ResolutionSettings
from sprites.characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from sprites.characters.utils.animation_utils import (
    create_animation_rects,
    set_animation_parameters,
    update_animation,
)
from sprites.characters.utils.check_cooldown import check_cooldown
from sprites.characters.utils.collision_utils import (
    is_below_collision,
    is_above_collision,
)
from sprites.characters.utils.normalize_direction import normalize_direction


class Bear(MovingEnemy):
    """
    Implementa un enemigo tipo oso en el juego. Este enemigo se mueve
    horizontalmente en las plataformas y puede saltar. Tiene puntos de
    salud que se reducen cuando recibe daño del jugador. A medida que
    recibe daño, aumenta su velocidad.
    """

    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        platform_rects,
        sprite_sheet_name,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            platform_rects,
            sprite_sheet_name,
            None,
        )

        self.resolution_settings = ResolutionSettings()
        self.difficulty_settings = DifficultySettings()
        self._setup_animation()

        self.rect = self.image.get_frect(topleft=pos)
        self.rect.width = self.resolution_settings.tile_size * 2

        self.speed = 190
        self.gravity = 1000
        self.fall = 0
        self.is_jumping = False
        self.jump_height = 320

        self.on_surface = True

        self.facing_right = True

        self.health_points = self.difficulty_settings.bear_health_points
        self.last_damage_time_ms = None

    def _setup_animation(self):
        set_animation_parameters(self)

        self.animations = {
            "run": create_animation_rects(
                0, 5, sprite_width=self.resolution_settings.tile_size * 2
            ),
            "jump": create_animation_rects(
                5, 1, sprite_width=self.resolution_settings.tile_size * 2
            ),
            "fall": create_animation_rects(
                6, 1, self.resolution_settings.tile_size * 2
            ),
        }

        self.current_animation = "run"
        self.facing_right = True

    def update(self, delta_time, environment_rects):
        self.environment_rects = environment_rects

        self._check_should_receive_damage()
        self._process_player_collision()

        self._determine_current_animation()
        update_animation(delta_time, self, self.animations[self.current_animation])

        self.old_rect = self.rect.copy()
        self.environment_rects = environment_rects
        self._move(delta_time)
        self._detect_platform_contact()

        self.facing_right = self.direction.x > 0

    def update_sprite(self):
        frame_rect = self.animations[self.current_animation][self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def _check_should_receive_damage(self):
        self.should_receive_damage = self._is_player_colliding_from_above()

    def _determine_current_animation(self):
        if self.is_jumping:
            self.current_animation = "fall" if self.fall > 0 else "jump"
        else:
            self.current_animation = "run"

        self.facing_right = self.direction.x > 0

    def _move(self, delta_time):
        self._move_horizontally(delta_time)
        self._move_vertically(delta_time)

    def _move_horizontally(self, delta_time):
        self.rect.x += self.direction.x * self._ratio * self.speed * delta_time

        if self._will_hit_wall():
            self.direction.x *= -1

        self.facing_right = self.direction.x > 0

    def _move_vertically(self, delta_time):
        self.rect.y += self.fall * self._ratio * delta_time
        self.fall += self.gravity * delta_time * self._ratio

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

        if is_above_collision(self.rect, self.old_rect, platform_rect):
            self.rect.top = platform_rect.bottom

        self.fall = 0
        self.direction.y = 0

    def _deal_damage_to_player(self):
        should_damage_player, _ = check_cooldown(self.last_damage_time_ms)

        if should_damage_player:
            super()._deal_damage_to_player()

    def _defeat(self):
        if self.health_points == 0:
            super()._defeat()

        self.is_jumping = True
        should_receive_damage, self.last_damage_time_ms = check_cooldown(
            self.last_damage_time_ms
        )

        if should_receive_damage:
            self.health_points -= 1
            self.speed += self.speed * 0.25
