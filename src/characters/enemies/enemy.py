from settings import *
from characters.character import Character
from resource_manager import ResourceManager
from pygame.sprite import collide_rect
from characters.players.collision_utils import is_below_collision


class Enemy(Character):
    def __init__(self, pos, surf, groups, player, platform_rects, sprite_sheet_name, animations, game):
        super().__init__(pos, surf, groups, platform_rects, sprite_sheet_name)
        self.groups = groups
        self.player = player
        self.animations = animations
        self.defeat_enemy_sound = ResourceManager.load_sound(
            "defeat_enemy.ogg")
        self.game = game

    def update(self, delta_time):
        super().update(delta_time)
        self._handle_collision_with_player()

    def _handle_collision_with_player(self):
        if not collide_rect(self, self.player):
            return

        self._adjust_player_position()

        is_player_colliding_from_above = is_below_collision(
            self.player.rect, self.player.old_rect, self.rect)

        if is_player_colliding_from_above or self.player.is_sprinting:
            self.defeat()
            return

        self.game.receive_damage()

    def defeat(self):
        for group in self.groups:
            if self in group:
                group.remove(self)

        self.defeat_enemy_sound.play()
        self.kill()

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

        self.player.collision()

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
