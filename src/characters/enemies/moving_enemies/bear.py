from characters.utils.check_cooldown import check_cooldown
from characters.utils.normalize_direction import normalize_direction
from characters.utils.collision_utils import is_below_collision
from characters.utils.animation_utils import (
    create_animation_rects,
    setup_animation,
    update_animation,
)
from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy


class Bear(MovingEnemy):
    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        platform_rects,
        sprite_sheet_name,
        game,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            platform_rects,
            sprite_sheet_name,
            None,
            game,
        )

        self._setup_animation()

        self.rect = self.image.get_frect(topleft=pos)
        self.rect.width = TILE_SIZE * 2

        self.speed = 100
        self.gravity = 1000
        self.fall = 0
        self.is_jumping = False
        self.jump_height = 250

        self.on_surface = True

        self.facing_right = True

        if DIFFICULTY == Difficulty.EASY:
            self.health_points = 3
        else:
            self.health_points = 5

        self.last_damage_time_ms = None

    def _setup_animation(self):
        setup_animation(self)

        self.animations = {
            "run": create_animation_rects(0, 5, sprite_width=TILE_SIZE * 2),
            "jump": create_animation_rects(5, 1, sprite_width=TILE_SIZE * 2),
            "fall": create_animation_rects(6, 1, TILE_SIZE * 2),
        }

        self.current_animation = "run"
        self.facing_right = True

    def update(self, delta_time, environment_rects):
        self.environment_rects = environment_rects

        self._check_should_receive_damage()
        self._process_player_collision()

        self._determine_current_animation()
        update_animation(delta_time, self,
                         self.animations[self.current_animation])

        self.old_rect = self.rect.copy()
        self.environment_rects = environment_rects
        self._move(delta_time)
        self._detect_platform_contact()

        self.facing_right = self.direction.x > 0

    def _check_should_receive_damage(self):
        self.should_receive_damage = self._is_player_colliding_from_above()

    def _determine_current_animation(self):
        if self.is_jumping:
            self.current_animation = "fall" if self.fall > 0 else "jump"
        else:
            self.current_animation = "run"

        self.facing_right = self.direction.x > 0

    def update_sprite(self):
        frame_rect = self.animations[self.current_animation][self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

    def _move(self, delta_time):
        self._move_horizontally(delta_time)
        self._move_vertically(delta_time)

    def _move_horizontally(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time

        if self._will_hit_wall():
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
