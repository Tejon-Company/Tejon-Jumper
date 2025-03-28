from characters.utils.check_cooldown import check_cooldown
from resource_manager import ResourceManager
from scene.game_over import GameOver
from singletons.director import Director
from singletons.settings.difficulty_settings import DifficultySettings
from singletons.settings.resolution_settings import ResolutionSettings
from singletons.singleton_meta import SingletonMeta
from ui.hud import HUD


class Game(metaclass=SingletonMeta):
    """
    Gestiona el estado global del juego, incluyendo la salud del jugador, vidas, monedas y efectos de sonido.
    """

    def __init__(self):
        self._director = Director()
        self._resolution_settings = ResolutionSettings()
        self._difficulty_settings = DifficultySettings()

        self._max_health_points = self._difficulty_settings.player_health_points
        self.health_points = self._max_health_points
        self.remaining_lives = self._difficulty_settings.player_lives
        self._player = None
        self.coins = 0

        self._last_damage_time_ms = None
        self._last_health_time_ms = None

        self._setup_sound_effects()
        HUD.initialize()

    def _setup_sound_effects(self):
        self._game_over_sound = ResourceManager.load_sound_effect("game_over.ogg")
        self._life_lost_sound = ResourceManager.load_sound_effect("life_lost.ogg")
        self._damage_sound = ResourceManager.load_sound_effect("damage.ogg")

    def handle_dead(self):
        if self.remaining_lives <= 0:
            self._game_over_sound.play()
            self._director.push_scene(GameOver())
            self.reload_game()
        else:
            self._life_lost_sound.play()
            self.remaining_lives -= 1
            self.health_points = self._max_health_points
            self.coins = 0

            self._restart_level()

    def _restart_level(self):
        from scene.level import Level

        current_scene = self._director.pop_scene()
        new_scene = Level(current_scene.current_level)
        self._director.change_scene(new_scene)

    def receive_damage(self, is_collision_on_left, is_collision_on_right):
        should_receive_damage, self._last_damage_time_ms = check_cooldown(
            self._last_damage_time_ms
        )

        if not should_receive_damage:
            return

        channel = self._damage_sound.play()
        effects_volume = ResourceManager.get_effects_volume()

        if is_collision_on_left:
            channel.set_volume(effects_volume, 0.0)
        elif is_collision_on_right:
            channel.set_volume(0.0, effects_volume)
        else:
            channel.set_volume(effects_volume, effects_volume)

        self.health_points -= 1

        if self.health_points <= 0:
            self.handle_dead()

    def add_coin(self):
        self.coins += 1

        if self.coins == 25:
            self.coins = 0
            self.remaining_lives += 1

    def heal(self):
        has_max_health = self.health_points == self._max_health_points
        should_receive_heal, self._last_health_time_ms = check_cooldown(
            self._last_health_time_ms
        )

        if not has_max_health and should_receive_heal:
            self.health_points += 1

    def reload_game(self):
        self.remaining_lives = self._difficulty_settings.player_lives
        self.health_points = self._max_health_points
        self.coins = 0

        self._last_damage_time_ms = None
        self._last_health_time_ms = None
