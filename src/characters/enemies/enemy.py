from abc import ABC
from typing import final

from pygame.sprite import collide_rect

from characters.character import Character
from resource_manager import ResourceManager
from singletons.game import Game


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
        self._groups = groups
        self._player = player
        self._sprite_sheet = ResourceManager.load_sprite_sheet(sprite_sheet_name)
        self._animations = animations
        self._defeat_enemy_sound = ResourceManager.load_sound_effect("defeat_enemy.ogg")
        self._game = Game()
        self._should_receive_damage = False

    def update(self, delta_time):
        super().update(delta_time)

        self._check_should_receive_damage()
        self._process_player_collision()

    def _check_should_receive_damage(self):
        self._should_receive_damage = (
            self._is_player_colliding_from_above()
            or self._player.is_sprinting
            or self._player.is_in_rage
        )

    def _is_player_colliding_from_above(self):
        approaching_from_top = self._player.rect.bottom >= self.rect.top
        was_above = self._player.old_rect.bottom <= self.old_rect.top
        return approaching_from_top and was_above

    @final
    def _process_player_collision(self):
        if not collide_rect(self, self._player):
            return

        self._adjust_player_position()

        if self._should_receive_damage:
            self._defeat()
        else:
            self._deal_damage_to_player()

    def _defeat(self):
        for group in self._groups:
            if self in group:
                group.remove(self)

        self._defeat_enemy_sound.play()
        self.kill()

    def _deal_damage_to_player(self):
        is_player_colliding_from_left = self._player.rect.centerx > self.rect.centerx
        is_player_colliding_from_right = self._player.rect.centerx < self.rect.centerx

        self._game.receive_damage(
            is_player_colliding_from_left, is_player_colliding_from_right
        )

    def _adjust_player_position(self):
        if not self._player.rect.colliderect(self.rect):
            return

        dif_x = abs(self._player.rect.centerx - self.rect.centerx)
        dif_y = abs(self._player.rect.centery - self.rect.centery)

        is_horizontal_collision = dif_x > dif_y

        if is_horizontal_collision:
            self._adjust_player_position_horizontally()
        else:
            self._adjust_player_position_vertically()

        self._player.handle_collisions_with_rects()

    def _adjust_player_position_horizontally(self):
        if self._player.rect.centerx < self.rect.centerx:
            self._player.rect.right = self.rect.left
        else:
            self._player.rect.left = self.rect.right

    def _adjust_player_position_vertically(self):
        is_player_above = self._player.rect.centery < self.rect.centery
        if is_player_above:
            self._player.rect.bottom = self.rect.top
        else:
            self._player.rect.top = self.rect.bottom

        horizontal_offset = 10
        is_player_left = self._player.rect.centerx < self.rect.centerx
        if is_player_left:
            self._player.rect.x -= horizontal_offset
        else:
            self._player.rect.x += horizontal_offset
