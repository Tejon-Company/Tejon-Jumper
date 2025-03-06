from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from random import choice
from characters.players.player_state import PlayerState

class Fox(MovingEnemy):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color="green")

        self.rect = self.image.get_frect(topleft=pos)

        self.direction = choice((-1, 1))
        self.speed = 75

    def handle_collision_with_player(self, level, player):
        player_state=None
        direction = self.get_collision_direction(player) 
        super().adjust_player_position(player)

        if player.is_sprinting:
            self.defeat()
        else:
            if direction in ["izquierda", "derecha", "arriba"]:
                player_state = player.receive_damage()
            elif direction == "abajo":
                self.defeat()


        match player_state:
            case PlayerState.ALIVE:
                pass
            case PlayerState.DAMAGED:
                level.ui.draw_hearts()
            case PlayerState.DEAD:
                level._handle_dead()

    def defeat(self):
        for group in self.groups:
            if isinstance(group, pygame.sprite.Group):
                if self in group:
                    group.remove(self)
        self.kill()