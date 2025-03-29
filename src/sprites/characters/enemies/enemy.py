from abc import ABC
from typing import final

from pygame.sprite import collide_rect

from resource_manager import ResourceManager
from singletons.game import Game
from sprites.characters.character import Character


class Enemy(Character, ABC):
    """
    Clase abstracta que implementa a un enemigo en el juego.
    Define el comportamiento básico de los enemigos, incluyendo la
    detección de colisiones con el jugador, la gestión de daño y su derrota.
    """

    def __init__(
        self,
        pos,
        surf,
        groups,
        player,
        platform_rects,
        sprite_sheet_name,
        animations,
    ):
        super().__init__(pos, surf, groups, platform_rects)
        self.groups = groups
        self.player = player
        self.sprite_sheet = ResourceManager.load_sprite_sheet(sprite_sheet_name)
        self.animations = animations
        self.defeat_enemy_sound = ResourceManager.load_sound_effect("defeat_enemy.ogg")
        self.game = Game()
        self.should_receive_damage = False

    def update(self, delta_time):
        super().update(delta_time)

        self._check_should_receive_damage()
        self._process_player_collision()

    def _check_should_receive_damage(self):
        self.should_receive_damage = (
            self._is_player_colliding_from_above()
            or self.player.is_sprinting
            or self.player.is_in_rage
        )

    def _is_player_colliding_from_above(self):
        approaching_from_top = self.player.rect.bottom >= self.rect.top
        was_above = self.player.old_rect.bottom <= self.old_rect.top
        return approaching_from_top and was_above

    @final
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
