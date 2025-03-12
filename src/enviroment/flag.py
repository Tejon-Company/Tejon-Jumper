from settings import *
from characters.players.player import Player
from enviroment.enviroment_element import Enviroment_element


class Flag(Enviroment_element):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


    def update(self, player: Player):
        if not self.rect.colliderect(player.rect):
            return
        
        self.kill()
