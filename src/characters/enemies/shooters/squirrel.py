from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool
from characters.players.player_state import PlayerState
from characters.players.collision_utils import is_below_collision


class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, player, sprite_sheet_name, animations, projectiles_pool=AcornPool):
        super().__init__(pos, surf, groups, player,
                         sprite_sheet_name, animations, projectiles_pool)

        self.rect = self.image.get_frect(topleft=pos)

        self._setup_animation()

    def handle_collision_with_player(self, level, player):
        if not pygame.sprite.collide_rect(self, player):
            return

        self.adjust_player_position(player)

        if is_below_collision(player.rect, player.old_rect, self.rect):
            self.defeat()
            return

        player_state = player.receive_damage()
        if player_state == PlayerState.DEAD:
            level.handle_dead()
