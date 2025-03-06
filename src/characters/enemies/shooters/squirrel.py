from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.acorn_pool import AcornPool
from characters.players.player_state import PlayerState

class Squirrel(Shooter):
    def __init__(self, pos, surf, groups, player, projectiles_pool=AcornPool):
        super().__init__(pos, surf, groups, player, projectiles_pool)

        self.rect = self.image.get_frect(topleft=pos)
    
    def handle_collision_with_player(self, level, player):
        player_state=None
        direction = self.get_collision_direction(player) 
        super().adjust_player_position(player)

        if player.is_sprinting:
            self.defeat()
        else:
            if direction in ["izquierda", "derecha", "arriba"]:
                player_state = player.receive_damage()
                if player_state == PlayerState.DEAD:
                    level.handle_dead()
            elif direction == "abajo":
                self.defeat()


    def defeat(self):
        for group in self.groups:  
            if isinstance(group, pygame.sprite.Group):
                if self in group:
                    group.remove(self)  
        self.kill()  

