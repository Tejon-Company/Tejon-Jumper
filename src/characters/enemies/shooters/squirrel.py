from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool
from characters.players.player_state import PlayerState
from characters.enemies.enemy_collision_directions import CollisionDirection

class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, player, projectiles_pool=AcornPool):
        super().__init__(pos, surf, groups, player, projectiles_pool)

        self.rect = self.image.get_frect(topleft=pos)
    
    def handle_collision_with_player(self, level, player):
        player_state = None
        direction = self.get_collision_direction(player)  # Esto devuelve un CollisionDirection Enum
        super().adjust_player_position(player)

        if player.is_sprinting or direction == CollisionDirection.BELOW:
            self.defeat()
        elif direction in [CollisionDirection.LEFT, CollisionDirection.RIGHT, CollisionDirection.ABOVE]:
            player_state = player.receive_damage()
            if player_state == PlayerState.DEAD:
                level.handle_dead()


