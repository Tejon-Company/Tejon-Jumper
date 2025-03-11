from settings import *
from scene.level import Level
from characters.players.player import Player

class Game:
    def __init__(self, director):
        self.director = director
        self.remaining_lives = 3
        self.coins = 0
        self.current_level = 1
        self._load_level()

    def _load_level(self):
        level_name = f"level{self.current_level}.tmx"
        self.level = Level(self.director, self.remaining_lives, "background1", "level_1.ogg", level_name)

    def _restart_level(self):
        self._load_level()

    def _game_over(self):
        self.director.exit_program()

    def events(self, event_list): 
        self.level.events(event_list)

    def update(self, delta_time):
        self.level.update(delta_time)
        self._check_player_state()

    def draw(self, surface): 
        self.level.draw(surface) 

    def _check_player_state(self):
        if self.level.player.health_points <= 0:
            self.remaining_lives -= 1
            if self.remaining_lives <= 0:
                self.level.handle_dead()
            else:
                self._restart_level()
