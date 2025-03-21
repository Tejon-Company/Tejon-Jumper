from settings import *
from characters.character import Character
from resource_manager import ResourceManager
from pygame.sprite import collide_rect
from abc import ABC, abstractmethod
from characters.utils.collision_utils import is_below_collision
from characters.utils.animation_utils import update_animation


class Enemy(Character, ABC):
    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        platform_rects,
        sprite_sheet_name,
        animations,
        game,
    ):
        super().__init__(pos, surf, groups, platform_rects)
        self.groups = groups
        self.player = player
        self.sprite_sheet = ResourceManager.load_sprite_sheet(sprite_sheet_name)
        self.animations = animations
        self.defeat_enemy_sound = ResourceManager.load_sound("defeat_enemy.ogg")
        self.game = game
        self.should_receive_damage = False

    def update(self, delta_time):
        super().update(delta_time)

        self._check_should_receive_damage()
        self._process_player_collision()

        update_animation(delta_time, self)

    def _check_should_receive_damage(self):
        is_player_colliding_from_above = is_below_collision(
            self.player.rect, self.player.old_rect, self.rect
        )

        self.should_receive_damage = (
            is_player_colliding_from_above
            or self.player.is_sprinting
            or self.player.is_in_rage
        )

    def _process_player_collision(self):
        if not collide_rect(self, self.player):
            return

        self._adjust_player_position()

        if self.should_receive_damage:
            self._defeat()
        else:
            self._deal_damage_to_player()

    def _defeat(self):
        for group in self.groups:
            if self in group:
                group.remove(self)

        self.defeat_enemy_sound.play()
        self.kill()

    def _deal_damage_to_player(self):
        is_player_colliding_from_left = self.player.rect.centerx > self.rect.centerx
        is_player_colliding_from_right = self.player.rect.centerx < self.rect.centerx

        self.game.receive_damage(
            is_player_colliding_from_left, is_player_colliding_from_right
        )

    def _adjust_player_position(self):
        if not self.player.rect.colliderect(self.rect):
            return

        dif_x = abs(self.player.rect.centerx - self.rect.centerx)
        dif_y = abs(self.player.rect.centery - self.rect.centery)

        is_horizontal_collision = dif_x > dif_y

        if is_horizontal_collision:
            self._adjust_player_position_horizontally()
        else:
            self._adjust_player_position_vertically()

        self.player.handle_collisions_with_rects()

    def _adjust_player_position_horizontally(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.player.rect.right = self.rect.left
        else:
            self.player.rect.left = self.rect.right

    def _adjust_player_position_vertically(self):
        is_player_above = self.player.rect.centery < self.rect.centery
        if is_player_above:
            self.player.rect.bottom = self.rect.top
        else:
            self.player.rect.top = self.rect.bottom

        horizontal_offset = 10
        is_player_left = self.player.rect.centerx < self.rect.centerx
        if is_player_left:
            self.player.rect.x -= horizontal_offset
        else:
            self.player.rect.x += horizontal_offset
