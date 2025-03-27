from os import listdir
from os.path import join

import pygame
from pygame.sprite import Group

from berries.berrie_factory import berry_factory
from characters.enemies.enemy_factory import enemy_factory
from characters.enemies.moving_enemies.bear import Bear
from characters.players.player import Player
from characters.sprite import Sprite
from environment.environment_factory import environment_factory
from projectiles.projectiles_pools.acorn_pool import AcornPool
from projectiles.projectiles_pools.spore_pool import SporePool
from resource_manager import ResourceManager
from scene.background import Background
from scene.camera import Camera
from scene.menus.pause_menu import PauseMenu
from scene.menus.victory_menu import VictoryMenu
from scene.scene import Scene
from singletons.director import Director
from singletons.game import Game
from singletons.settings.resolution_settings import ResolutionSettings
from ui.hud import HUD


class Level(Scene):
    _levels_config = {
        1: {
            "background": "background1",
            "music": "level_1.ogg",
            "map": "level1.tmx",
            "map_size": 121,
        },
        2: {
            "background": "background2",
            "music": "level_2.ogg",
            "map": "level2.tmx",
            "map_size": 154,
        },
        3: {
            "background": "background3",
            "music": "level_3.ogg",
            "map": "level3.tmx",
            "map_size": 113,
        },
    }

    def __init__(
        self,
        current_level: int,
    ):
        super().__init__()

        self.resolution_settings = ResolutionSettings()
        self.director = Director()
        self.game = Game()
        self.current_level = current_level

        self.is_on_pause = False

        self.tmx_map = ResourceManager.load_tmx_map(
            self._levels_config[self.current_level]["map"]
        )

        self._setup_groups()
        self.backgrounds = []
        self._setup_pools()
        self._setup_camera()

        self._setup_background(self._levels_config[self.current_level]["background"])

        self._setup_layer("Background", "backgrounds")
        self._setup_layer("Terrain", "platforms")
        self._setup_layer("Deco", "deco")

        self._setup_platform_rects()

        self._setup_player()
        self._setup_enemies()
        self._setup_boss()
        self._setup_environment()

        self._setup_platform_rects()
        self.player.set_platform_rects(self.platform_rects)

        self._setup_berries()

        Scene._setup_music(self._levels_config[self.current_level]["music"])

    def _setup_groups(self):
        self.groups = {
            "shooters": Group(),
            "platforms": Group(),
            "characters": Group(),
            "backgrounds": Group(),
            "projectiles": Group(),
            "berries": Group(),
            "deco": Group(),
            "environment": Group(),
            "moving_enemies": Group(),
        }

    def _setup_pools(self):
        self.spore_pool = SporePool(20, self.groups["projectiles"])
        self.acorn_pool = AcornPool(20, self.groups["projectiles"])

    def _setup_camera(self):
        map_width = self.tmx_map.width * self.resolution_settings.tile_size
        map_height = self.tmx_map.height * self.resolution_settings.tile_size
        self.camera = Camera(map_width, map_height)

    def _setup_background(self, background):
        background_folder = join("assets", "hd", "backgrounds", "day", background)
        image_files = self._get_image_files(background_folder)
        parallax_factor = [0.1, 0.2, 0.4, 0.9]

        for i, image_name in enumerate(image_files):
            self.backgrounds.append(
                Background(
                    join(background_folder, image_name),
                    (0, 0),
                    parallax_factor[i % len(parallax_factor)],
                )
            )

    @staticmethod
    def _get_image_files(background_folder):
        image_files = []
        for file in listdir(background_folder):
            if file.endswith(".png"):
                image_files.append(file)

        image_files.sort(key=lambda file_name: int(file_name.split(".")[0]))

        return image_files

    def _setup_layer(self, layer_name, group_key):
        for x, y, surf in self.tmx_map.get_layer_by_name(layer_name).tiles():
            Sprite(
                (
                    x * self.resolution_settings.tile_size,
                    y * self.resolution_settings.tile_size,
                ),
                surf,
                self.groups[group_key],
            )

    def _setup_player(self):
        player_layer = self.tmx_map.get_layer_by_name("Player")
        player_count = len(list(player_layer))

        if player_count != 1:
            raise ValueError(
                f"Expected exactly one player in the map, found {player_count}"
            )

        character = next(iter(player_layer))
        self.player = Player(
            (character.x, character.y),
            character.image,
            self.groups["characters"],
            self._levels_config[self.current_level]["map_size"],
        )

    def _setup_enemies(self):
        for enemy in self.tmx_map.get_layer_by_name("Enemies"):
            enemy_factory(
                enemy,
                self.groups,
                self.platform_rects,
                self.spore_pool,
                self.acorn_pool,
                self.player,
            )

    def _setup_boss(self):
        try:
            boss_layer = self.tmx_map.get_layer_by_name("Boss")
            for boss in boss_layer:
                self.boss = Bear(
                    (boss.x, boss.y),
                    boss.image,
                    (self.groups["moving_enemies"], self.groups["characters"]),
                    self.player,
                    self.platform_rects,
                    "bear.png",
                )
        except ValueError:
            self.boss = None

    def _setup_platform_rects(self):
        self.platform_rects = [platform.rect for platform in self.groups["platforms"]]

    def _setup_berries(self):
        for berrie in self.tmx_map.get_layer_by_name("Berries"):
            berry_factory(berrie, self.groups["berries"])

    def _setup_environment(self):
        for map_element in self.tmx_map.get_layer_by_name("Environment"):
            environment_factory(
                map_element, self.groups["environment"], self.player, self
            )

    def go_to_next_level(self):
        number_of_levels = len(self._levels_config)
        next_level_index = self.current_level + 1 % number_of_levels

        if next_level_index > number_of_levels:
            boss_has_been_defeated = not self.boss.alive()
            self.director.change_scene(VictoryMenu(boss_has_been_defeated))

        else:
            next_level = Level(next_level_index)
            self.director.change_scene(next_level)

    def update(self, delta_time):
        if self.is_on_pause:
            return

        self.groups["environment"].update()
        environment_rects = [platform.rect for platform in self.groups["environment"]]

        self.player.update(delta_time, environment_rects)
        self.groups["projectiles"].update(delta_time, self.player)
        self.groups["moving_enemies"].update(delta_time, environment_rects)
        self.groups["shooters"].update(delta_time)
        self.groups["berries"].update(self.player)

        self.camera.update(self.player)

    def events(self, events_list):
        keys = pygame.key.get_just_released()

        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif keys[pygame.K_p]:
                self.is_on_pause = not self.is_on_pause
                self.director.push_scene(PauseMenu())
                self.is_on_pause = False

    def draw(self, display_surface):
        self.camera.draw_background(self.backgrounds, display_surface)

        self._draw_group(display_surface, "backgrounds")
        self._draw_group(display_surface, "deco")
        self._draw_group(display_surface, "platforms")
        self._draw_group(display_surface, "characters")
        self._draw_group(display_surface, "environment")

        for projectile in self.groups["projectiles"]:
            if projectile.is_activated:
                display_surface.blit(projectile.image, self.camera.apply(projectile))

        self._draw_group(display_surface, "berries")

        HUD.draw_hud(
            display_surface,
            self.game.health_points,
            self.game.remaining_lives,
            self.game.coins,
            self.player.energy,
            self.boss.health_points if self.boss else 0,
        )

    def _draw_group(self, display_surface, group):
        for sprite in self.groups[group]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))
