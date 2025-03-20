from settings import *
from scene.level import Level
from scene.game_over import GameOver
from resource_manager import ResourceManager
from ui.hud import HUD
from scene.pause import Pause
from characters.utils.check_cooldown import check_cooldown


class Game:
    def __init__(self, director):
        self.director = director
        self.remaining_lives = 3
        self.max_health_points = 5
        self.health_points = self.max_health_points
        self.player = None
        self.coins = 0
        self.current_level = 1
        self.is_on_pause = False

        self.last_damage_time_ms = None
        self.last_health_time_ms = None

        self.damage_sound = ResourceManager.load_sound("damage.ogg")

        HUD.initialize()

        self._load_level()

    def _load_level(self):
        level_name = f"level{self.current_level}.tmx"
        level_background = f"background{self.current_level}"
        level_music = f"level_{self.current_level}.ogg"
        self.level = Level(self.director,
                           level_background, level_music, level_name, self)
        self.player = self.level.player
        self._setup_sound_effects()

    def _setup_sound_effects(self):
        self.game_over_sound = ResourceManager.load_sound("game_over.ogg")
        self.life_lost_sound = ResourceManager.load_sound("life_lost.ogg")

    def events(self, event_list):
        self.level.events(event_list)

    def update(self, delta_time):
        self.level.update(delta_time)
        self._handle_fall()

        for berry in self.level.groups.get("berries", []):
            berry.update(self, self.player)

    def _handle_fall(self):
        if self.player.rect.bottom > WINDOW_HEIGHT:
            self._handle_dead()

    def _handle_dead(self):
        if self.remaining_lives <= 0:
            self.game_over_sound.play()
            self.director.stack_scene(GameOver(self.director))
        else:
            self.life_lost_sound.play()
            self.remaining_lives -= 1
            self.health_points = self.max_health_points
            self.coins = 0

            self._restart_level()

    def _restart_level(self):
        self._load_level()

    def receive_damage(self):
        should_receive_damage, self.last_damage_time_ms = check_cooldown(
            self.last_damage_time_ms)

        if not should_receive_damage:
            return False

        self.damage_sound.play()
        self.health_points -= 1

        if (self.health_points <= 0):
            self._handle_dead()

        return self.health_points <= 0

    def add_coin(self):
        self.coins += 1

        if self.coins == 25:
            self.coins = 0
            self.remaining_lives += 1

    def heal(self):
        has_max_health = self.health_points == self.max_health_points
        should_receive_heal, self.last_health_time_ms = check_cooldown(
            self.last_health_time_ms)

        if not has_max_health and should_receive_heal:
            self.health_points += 1

    def change_current_level(self):
        if self.current_level == 3:
            self.current_level = 1
            return

        self.current_level += 1
        self._load_level()

    def draw(self, surface):
        self.level.draw(surface)

    def _game_over(self):
        self.director.exit_program()
