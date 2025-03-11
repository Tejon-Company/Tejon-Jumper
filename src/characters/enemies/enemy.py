from settings import *
from characters.character import Character
from resource_manager import ResourceManager
from characters.players.player import Player
from characters.players.player_state import PlayerState
from characters.players.collision_utils import is_below_collision


class Enemy(Character):
    def __init__(self, pos, surf, groups, sprite_sheet_name, animations):
        super().__init__(pos, surf, groups, sprite_sheet_name)
        self.groups = groups
        self.animations = animations
        self.defeat_enemy_sound = ResourceManager.load_sound(
            "defeat_enemy.ogg")

    def _setup_animation(self):
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0

    def handle_collision_with_player(self, level, player):
        pass

    def defeat(self):
        for group in self.groups:
            if self in group:
                group.remove(self)

        self.defeat_enemy_sound.play()
        self.kill()

    def handle_collision_with_player(self, level, player):
        if not pygame.sprite.collide_rect(self, player):
            return

        self._adjust_player_position(player)

        if is_below_collision(player.rect, player.old_rect, self.rect) or player.is_sprinting:
            self.defeat()
            return

        player_state = player.receive_damage()
        if player_state == PlayerState.DEAD:
            level.handle_dead()

    def _adjust_player_position(self, player: Player):
        if not player.rect.colliderect(self.rect):
            return

        dif_x = abs(player.rect.centerx - self.rect.centerx)
        dif_y = abs(player.rect.centery - self.rect.centery)

        is_horizontal_collision = dif_x > dif_y

        if is_horizontal_collision:
            player.handle_horizontal_collision(self.rect)
        else:
            player.handle_vertical_collision(self.rect)
