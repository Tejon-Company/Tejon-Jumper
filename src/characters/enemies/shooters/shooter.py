from settings import *
from characters.enemies.enemy import Enemy
from projectiles.projectiles_pools.projectiles_pool import ProjectilesPool
from characters.utils.animation_utils import update_animation, setup_animation
from abc import ABC


class Shooter(Enemy, ABC):
    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        sprite_sheet_name,
        animations,
        game,
        projectiles_pool=ProjectilesPool,
    ):
        super().__init__(
            pos, surf, groups, player, None, sprite_sheet_name, animations, game
        )
        self.shoot_cooldown = 3000
        self.pos = pos
        self.last_shot = 0
        self.player = player
        self.projectiles_pool = projectiles_pool
        self.is_shooting = False
        self.shooting_timer = 0
        self.shooting_duration = 500
        setup_animation(self)

    def update(self, delta_time):
        super().update(delta_time)

        self._shoot()

    def _shoot(self):
        current_time = pygame.time.get_ticks()
        cooldown_passed = current_time - self.last_shot >= self.shoot_cooldown
        is_shooting = cooldown_passed and self._is_player_near()

        if is_shooting:
            self.is_shooting = True
            self.projectiles_pool.shoot(self.pos[0], self.pos[1])
            self.last_shot = current_time

    def _is_player_near(self):
        player_pos, projectile_pos = vector(self.player.rect.center)
        projectile_pos = vector(self.rect.center)

        return projectile_pos.distance_to(player_pos) < 500

    def update_sprite(self):
        frame_rect = self.animations[self.animation_frame]
        self.image = self.sprite_sheet.subsurface(frame_rect)

        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)
