from characters.sprite import Sprite
from characters.players.player import Player
from abc import abstractmethod


class Enviroment_element(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.image = surf

        self.rect = self.image.get_frect(topleft=pos)

    @abstractmethod
    def update(self, player: Player):
        pass
    def handle_collision_with_player(self, level, player):
        pass

    def defeat(self):
        for group in self.groups:
            if self in group:
                group.remove(self)

        self.kill()

    def adjust_player_position(self, player):
        if not player.rect.colliderect(self.rect):
            return
        dif_x = abs(player.rect.centerx - self.rect.centerx)
        dif_y = abs(player.rect.centery - self.rect.centery)

        is_horizontal_collision = dif_x > dif_y

        if is_horizontal_collision:
            self._adjust_player_position_horizontally(player)
        else:
            self._adjust_player_position_vertically(player)

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
