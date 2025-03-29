from enum import Enum, auto
from sprites.characters.enemies.shooters.shooter import Shooter
from sprites.projectiles.projectiles_pools.spore_pool import SporePool
import pygame


class Mushroom(Shooter):
    class MushroomState(Enum):
        IDLE = auto()
        PREPARING = auto()
        SHOOTING = auto()

    def __init__(
        self,
        pos,
        surf,
        groups,
        direction,
        player,
        sprite_sheet_name,
        animations,
        projectiles_pool=SporePool,
    ):
        super().__init__(
            pos,
            surf,
            groups,
            player,
            sprite_sheet_name,
            animations,
            projectiles_pool,
        )
        self.direction = direction
        self.shoot_cooldown = 5000
        self.rect = self.image.get_frect(topleft=pos)

        self.pre_shoot_duration = 500
        self.shooting_duration = 300

        self.current_state = self.MushroomState.IDLE
        self.state_timer = 0

    def update(self, delta_time):
        super().update(delta_time)

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        had_cooldown_passed = current_time - self.last_shot >= self.shoot_cooldown

        if had_cooldown_passed and self._is_player_near():
            self.current_state = self.MushroomState.PREPARING
            self.state_timer = 0
            self.last_shot = current_time

    def _update_animation_frame(self, delta_time):
        delta_ms = delta_time * 1000

        if self.current_state == self.MushroomState.PREPARING:
            self._handle_preparing_state(delta_ms)
        elif self.current_state == self.MushroomState.SHOOTING:
            self._handle_shooting_state(delta_ms)
        else:
            self.animation_frame = 0

    def _handle_preparing_state(self, delta_ms):
        self.state_timer += delta_ms
        self.animation_frame = 1
        is_ready_to_shoot = self.state_timer >= self.pre_shoot_duration

        if is_ready_to_shoot:
            self.current_state = self.MushroomState.SHOOTING
            self.state_timer = 0

    def _handle_shooting_state(self, delta_ms):
        self.state_timer += delta_ms
        is_shooting_ready = self.state_timer >= self.shooting_duration

        if is_shooting_ready:
            self.projectiles_pool.shoot(self.pos[0], self.pos[1], self.direction, )
            self.current_state = self.MushroomState.IDLE
            self.state_timer = 0
        else:
            is_ready_for_next_frame = self.state_timer >= self.shooting_duration * 0.1
            self.animation_frame = 2 if is_ready_for_next_frame else 1
