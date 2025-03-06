from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.spore_pool import SporePool
from characters.players.player_state import PlayerState


class Mushroom(Shooter):
    def __init__(self, pos, surf, groups, projectiles_pool=SporePool):
        super().__init__(pos, surf, groups, projectiles_pool)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="pink")

        self.rect = self.image.get_frect(topleft=pos)

    def handle_collision_with_player(self, level, player):
        pass

    def defeat(self):
        pass
