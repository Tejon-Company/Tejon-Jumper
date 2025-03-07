from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.players.player_state import PlayerState
from characters.players.collision_utils import is_above_collision,is_left_collision, is_right_collision



class Hedgehog(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 50

    def handle_collision_with_player(self, level, player):

        if not pygame.sprite.collide_rect(self, player):
            return 

        self.adjust_player_position(player)

        if player.is_sprinting and (
            is_left_collision(player.rect, player.old_rect, self.rect) or
            is_right_collision(player.rect, player.old_rect, self.rect) or
            is_above_collision(player.rect, player.old_rect, self.rect)
        ):
            self.defeat() 
            return 

        player_state = player.receive_damage()
        if player_state == PlayerState.DEAD:
            level.handle_dead()  
