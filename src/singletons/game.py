from settings import *
from scene.game_over import GameOver
from resource_manager import ResourceManager
from ui.hud import HUD
from characters.utils.check_cooldown import check_cooldown
from singletons.singleton_meta import SingletonMeta
from singletons.director import Director


class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.director = Director()
        self.remaining_lives = 3
        self.max_health_points = 5
        self.health_points = self.max_health_points
        self.player = None
        self.coins = 0
        self.current_level = 1

        self.last_damage_time_ms = None
        self.last_health_time_ms = None

        self._setup_sound_effects()
        HUD.initialize(TILE_SIZE, 22)

    def _setup_sound_effects(self):
        self.game_over_sound = ResourceManager.load_sound_effect("game_over.ogg")
        self.life_lost_sound = ResourceManager.load_sound_effect("life_lost.ogg")
        self.damage_sound = ResourceManager.load_sound_effect("damage.ogg")

    def handle_dead(self):
        if self.remaining_lives <= 0:
            self.game_over_sound.play()
            self.director.push_scene(GameOver(self.director))
        else:
            self.life_lost_sound.play()
            self.remaining_lives -= 1
            self.health_points = self.max_health_points
            self.coins = 0

            self._restart_level()

    def _restart_level(self):
        current_scene = self.director.pop_scene()

    def receive_damage(self, is_collision_on_left, is_collision_on_right):
        should_receive_damage, self.last_damage_time_ms = check_cooldown(
            self.last_damage_time_ms
        )

        if not should_receive_damage:
            return

        channel = self.damage_sound.play()
        effects_volume = ResourceManager.get_effects_volume()

        if is_collision_on_left:
            channel.set_volume(effects_volume, 0.0)
        elif is_collision_on_right:
            channel.set_volume(0.0, effects_volume)
        else:
            channel.set_volume(effects_volume, effects_volume)

        self.health_points -= 1

        if self.health_points <= 0:
            self._handle_dead()

    def add_coin(self):
        self.coins += 1

        if self.coins == 25:
            self.coins = 0
            self.remaining_lives += 1

    def heal(self):
        has_max_health = self.health_points == self.max_health_points
        should_receive_heal, self.last_health_time_ms = check_cooldown(
            self.last_health_time_ms
        )

        if not has_max_health and should_receive_heal:
            self.health_points += 1

    def _game_over(self):
        self.director.exit_program()
