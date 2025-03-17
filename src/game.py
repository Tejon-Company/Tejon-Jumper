from settings import *
from characters.enemies.moving_enemies.moving_enemy import MovingEnemy
from scene.level import Level
from scene.game_over import GameOver
from resource_manager import ResourceManager
from pygame.sprite import spritecollide
from scene.pause import Pause


class Game:
    def __init__(self, director):
        self.director = director
        self.remaining_lives = 3
        self.player = None
        self.coins = 0
        self.current_level = 1
        self.is_on_pause = False

        self.last_damage_time_ms = None
        self.last_health_time_ms = None

        self.damage_sound = ResourceManager.load_sound("damage.ogg")

        self._load_level()

    def _load_level(self):
        level_name = f"level{self.current_level}.tmx"
        level_background = f"background{self.current_level}"
        # level_music = f"level_{self.current_level}.ogg"
        level_music = "level_1.ogg"
        self.level = Level(self.director, self.remaining_lives,
                           level_background, level_music, level_name, self)
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
        if self._is_game_paused():
            return
        self.level.update(delta_time)
        self._handle_player_collisions()
        self._handle_fall()
        self._handle_flag_collision()

    def _handle_player_collisions(self):
        if spritecollide(self.player, self.level.groups["projectiles"], True):
            self.receive_damage()

        for enemy in self.level.groups.get("enemies", []):
            if isinstance(enemy, MovingEnemy):
                enemy.update(0)
            enemy.handle_collision_with_player(self, self.player)

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

            self._restart_level()

    def receive_damage(self):
        should_receive_damage, self.last_damage_time_ms = self._check_cooldown(
            self.last_damage_time_ms)

        if not should_receive_damage:
            return False

        self.damage_sound.play()
        self.player.health_points -= 1

        if (self.player.health_points <= 0):
            self._handle_dead()

        return self.player.health_points <= 0

    def _check_cooldown(self, last_time_ms):
        current_time_ms = pygame.time.get_ticks()

        if not last_time_ms:
            return True, current_time_ms

        if current_time_ms < last_time_ms + 2000:
            return False, last_time_ms

        return True, current_time_ms

    def draw(self, surface):
        self.level.draw(surface)

    def change_current_level(self):
        if self.current_level == 3:
            self.current_level = 1
            return

        self.current_level += 1
        self._load_level()

    def _is_game_paused(self):
        keys = pygame.key.get_just_released()

        if keys[pygame.K_p]:
            self.is_on_pause = not self.is_on_pause
            self.director.stack_scene(Pause(self.director))
            self.is_on_pause = False

        return self.is_on_pause

    def _handle_flag_collision(self):
        if self.level.flag.rect.colliderect(self.player.rect):
            self.change_current_level()
