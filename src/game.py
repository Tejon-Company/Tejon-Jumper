from settings import *
from scene.level import Level
from scene.game_over import GameOver
from resource_manager import ResourceManager


class Game:
    def __init__(self, director):
        self.director = director
        self.remaining_lives = 3
        self.player = None
        self.coins = 0
        self.current_level = 1
        self._load_level()

    def _load_level(self):
        level_name = f"level{self.current_level}.tmx"
        self.level = Level(self.director, self.remaining_lives,
                           "background1", "level_1.ogg", level_name, self)
        self.player = self.level.player
        self._setup_sound_effects()

    def _setup_sound_effects(self):
        self.game_over_sound = ResourceManager.load_sound("game_over.ogg")
        self.life_lost_sound = ResourceManager.load_sound("life_lost.ogg")

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
        if self.player.health_points <= 0:
            self.remaining_lives -= 1
            action = self.handle_dead if self.remaining_lives <= 0 else self._restart_level
            action()

    def handle_dead(self):
        if self.remaining_lives <= 0:
            self.game_over_sound.play()
            self.director.stack_scene(GameOver(self.director))
        else:
            self.life_lost_sound.play()
            self.remaining_lives -= 1

            self._restart_level()
