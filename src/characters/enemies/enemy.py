from settings import *
from characters.character import Character
from resource_manager import ResourceManager
from characters.players.player import Player
from pygame.sprite import collide_rect
from characters.players.collision_utils import is_below_collision


class Enemy(Character):
    def __init__(self, pos, surf, groups, platform_rects, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, platform_rects, sprite_sheet_name)
        self.groups = groups
        self.animations = animations
        self.defeat_enemy_sound = ResourceManager.load_sound(
            "defeat_enemy.ogg")

    def _setup_animation(self):
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0

    def handle_collision_with_player(self, game, player):
        if not collide_rect(self, player):
            return

        self._adjust_player_position(player)

        is_player_colliding_from_above = is_below_collision(
            player.rect, player.old_rect, self.rect)

        if is_player_colliding_from_above or player.is_sprinting:
            self.defeat()
            return

        game.receive_damage()

    def defeat(self):
        for group in self.groups:
            if self in group:
                group.remove(self)

        self.defeat_enemy_sound.play()
        self.kill()

    def _adjust_player_position(self, player: Player):
        if not player.rect.colliderect(self.rect):
            return
        dif_x = abs(player.rect.centerx - self.rect.centerx)
        dif_y = abs(player.rect.centery - self.rect.centery)

        is_horizontal_collision = dif_x > dif_y

        if is_horizontal_collision:
            self._adjust_player_position_horizontally(player)
        else:
            self._adjust_player_position_vertically(player)
        player.collision()

    def _adjust_player_position_horizontally(self, player):
        if player.rect.centerx < self.rect.centerx:
            player.rect.right = self.rect.left
        else:
            player.rect.left = self.rect.right

    def _adjust_player_position_vertically(self, player):
        is_player_above = player.rect.centery < self.rect.centery
        if is_player_above:
            player.rect.bottom = self.rect.top
        else:
            player.rect.top = self.rect.bottom

        horizontal_offset = 10
        is_player_left = player.rect.centerx < self.rect.centerx
        if is_player_left:
            player.rect.x -= horizontal_offset
        else:
            player.rect.x += horizontal_offset
