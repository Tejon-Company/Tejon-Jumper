from enviroment.enviroment_element import Enviroment_element
from characters.players.player import Player
from characters.players.collision_utils import is_below_collision

from pygame.sprite import collide_rect

class Rock(Enviroment_element):
    
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return

    
    def handle_collision_with_player(self, player):
        if not collide_rect(self, player):
            return
        
        if player.is_sprinting:
            self.defeat()
            return
        
        
        
        self.adjust_player_position(player)

  


