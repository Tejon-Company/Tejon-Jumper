from settings import *
from characters.enemies.shooters.shooter import Shooter
from projectiles.projectiles_pools.spore_pool import SporePool
from characters.players.player_state import PlayerState


class Mushroom(Shooter):
    def __init__(self, pos, surf, groups, player, projectiles_pool=SporePool):
        super().__init__(pos, surf, groups, player, projectiles_pool)
        self.shoot_cooldown = 5000

        self.rect = self.image.get_frect(topleft=pos)
