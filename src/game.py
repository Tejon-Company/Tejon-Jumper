from characters.players.player import Player
from characters.players.player_state import PlayerState
from scene.level import Level
from resource_manager import ResourceManager
from scene.game_over import game_over
from settings import *


class Game:
    def __init__(self, director, level: str = "level1.tmx", background: str = "background1", music: str = "level_1.ogg"):
        self.director = director
        self.level_name = level
        self.background = background
        self.music = music
        self.remaining_lives = 3
        self.current_level = None
        self.player = None

        self._setup_level()

    def _setup_level(self):
        self.current_level = Level(
            self.director, self.remaining_lives, self.background, self.music, self.level_name)
        self.player = self.current_level.player

    def update(self, delta_time):
        self.current_level.update(delta_time)

        if self.player.health_points <= 0:
            self.handle_dead()

    def handle_dead(self):
        if self.remaining_lives <= 0:
            self.director.stack_scene(game_over(self.director))
        else:
            self.remaining_lives -= 1
            self.director.stack_scene(
                Level(self.director, self.remaining_lives))

    def events(self, events_list):
        self.current_level.events(events_list)

    def draw(self, display_surface):
        self.current_level.draw(display_surface)
