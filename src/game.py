from settings import *
from scene.level import Level
from scene.game_over import GameOver
from resource_manager import ResourceManager
from characters.players.player_state import PlayerState
from pygame.sprite import Group, spritecollide, collide_rect


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
        level_background = f"background{self.current_level}"
        self.level = Level(self.director, self.remaining_lives,
                           level_background, "level_1.ogg", level_name, self)
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
        self._handle_player_collisions()
        self.handle_fall()
        self.check_game_state()

    def _handle_player_collisions(self):
        if spritecollide(self.player, self.level.groups["projectiles"], True):
            self._handle_projectile_collision()
        elif spritecollide(self.player, self.level.groups["enemies"], False):
            self._handle_enemy_collision()

    def _handle_enemy_collision(self):
        enemies = self.level.groups.get("enemies", [])

        for enemy in enemies:
            if not collide_rect(self.player, enemy):
                continue

            if enemy.handle_collision_with_player(self, self.player) == PlayerState.DEAD:
                self.handle_dead()
                return

    def _handle_projectile_collision(self):
        if self.player.receive_damage() == PlayerState.DEAD:
            self.handle_dead()

    def handle_fall(self):
        if self.player.rect.bottom > WINDOW_HEIGHT:
            self.handle_dead()

    def handle_dead(self):
        if self.remaining_lives <= 0:
            self.game_over_sound.play()
            self.director.stack_scene(GameOver(self.director))
        else:
            self.life_lost_sound.play()
            self.remaining_lives -= 1

            self._restart_level()

    def draw(self, surface):
        self.level.draw(surface)

    def change_current_level(self):
        if self.current_level == 3:
            self.current_level = 1
            return

        self.current_level += 1
        self._load_level

    def check_game_state(self):
        if self.player.health_points > 0:
            return

        self.remaining_lives -= 1

        if self.remaining_lives <= 0:
            self.handle_dead()
        else:
            self._restart_level()
