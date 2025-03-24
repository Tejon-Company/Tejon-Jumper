from settings import *
from characters.sprite import Sprite
from characters.players.player import Player
from characters.enemies.moving_enemies.bear import Bear
from pygame.sprite import Group
from characters.enemies.enemy_factory import enemy_factory
from scene.background import Background
from scene.camera import Camera
from projectiles.projectiles_pools.acorn_pool import AcornPool
from projectiles.projectiles_pools.spore_pool import SporePool
from environment.environment_factory import environment_factory
from berries.berrie_factory import berry_factory
from scene.scene import Scene
from pytmx.util_pygame import load_pygame
from director import Director
from os import listdir
from ui.hud import HUD


class Level(Scene):
    def __init__(
        self,
        director: Director,
        background: str,
        music: str,
        level: str,
        game=None,
    ):
        super().__init__(director)

        self.game = game

        level_path = join("assets", "maps", "levels", level)
        self.tmx_map = load_pygame(level_path)

        self._setup_groups()
        self._setup_pools()
        self._setup_camera()

        self._setup_background(background)
        self._setup_tiled_background()
        self._setup_terrain()
        self._setup_deco()

        self._setup_platform_rects()

        self._setup_player()
        self._setup_enemies()
        self._setup_boss()
        self._setup_environment()

        self._setup_platform_rects()

        self.player.set_platform_rects(self.platform_rects)
        self._setup_berries()

        Scene._setup_music(music)

    def _setup_groups(self):
        self.groups = {
            "all_sprites": Group(),
            "platforms": Group(),
            "enemies": Group(),
            "backgrounds": [],
            "projectiles": Group(),
            "berries": Group(),
            "tiled_backgrsound": Group(),
            "deco": Group(),
            "environment": Group(),
            "players": Group(),
            "moving_enemies": Group(),
        }

    def _setup_pools(self):
        self.spore_pool = SporePool(20, self.groups["projectiles"], self.game)
        self.acorn_pool = AcornPool(20, self.groups["projectiles"], self.game)

    def _setup_camera(self):
        map_width = self.tmx_map.width * TILE_SIZE
        map_height = self.tmx_map.height * TILE_SIZE
        self.camera = Camera(map_width, map_height)

    def _setup_background(self, background):
        background_folder = join("assets", "maps", "backgrounds", background)
        image_files = self._get_image_files(background_folder)

        for i, image_name in enumerate(image_files):
            Background(
                join(background_folder, image_name),
                (0, 0),
                PARALLAX_FACTOR[i % len(PARALLAX_FACTOR)],
                self.groups["backgrounds"],
            )

    @staticmethod
    def _get_image_files(background_folder):
        image_files = []
        for file in listdir(background_folder):
            if file.endswith(".png"):
                image_files.append(file)

        image_files.sort(key=lambda file_name: int(file_name.split(".")[0]))

        return image_files

    def _setup_tiled_background(self):
        for x, y, surf in self.tmx_map.get_layer_by_name("Background").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["all_sprites"]),
            )

    def _setup_terrain(self):
        for x, y, surf in self.tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["all_sprites"], self.groups["platforms"]),
            )

    def _setup_deco(self):
        for x, y, surf in self.tmx_map.get_layer_by_name("Deco").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["deco"]),
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
            (character.x, character.y), character.image, self.groups["players"]
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
                self.game,
            )

    def _setup_boss(self):
        try:
            boss_layer = self.tmx_map.get_layer_by_name("Boss")
            for boss in boss_layer:
                self.boss = Bear(
                    (boss.x, boss.y),
                    boss.image,
                    (self.groups["moving_enemies"], self.groups["enemies"]),
                    self.player,
                    self.platform_rects,
                    "bear.png",
                    self.game,
                )
        except ValueError:
            self.boss = None

    def _setup_platform_rects(self):
        self.platform_rects = [platform.rect for platform in self.groups["platforms"]]

    def _setup_berries(self):
        for berrie in self.tmx_map.get_layer_by_name("Berries"):
            berry_factory(berrie, self.groups)

    def _setup_environment(self):
        for map_element in self.tmx_map.get_layer_by_name("Environment"):
            environment_factory(map_element, self.groups, self.player, self.game)

    def update(self, delta_time):
        self.groups["environment"].update()
        environment_rects = [platform.rect for platform in self.groups["environment"]]

        self.groups["all_sprites"].update(delta_time)
        self.groups["players"].update(delta_time, environment_rects)
        self.groups["moving_enemies"].update(delta_time, environment_rects)

        self.groups["projectiles"].update(delta_time, self.player)

        self.camera.update(self.player)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()

    def draw(self, display_surface):
        self.camera.draw_background(self.groups["backgrounds"], display_surface)

        for sprite in self.groups["deco"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["all_sprites"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["players"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["moving_enemies"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["environment"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for projectile in self.groups["projectiles"]:
            if projectile.is_activated:
                display_surface.blit(projectile.image, self.camera.apply(projectile))

        for sprite in self.groups["berries"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        if self.boss:
            HUD.draw_hud(
                display_surface,
                self.game.health_points,
                self.game.remaining_lives,
                self.game.coins,
                self.game.player.energy,
                self.boss.health_points,
            )
        else:
            HUD.draw_hud(
                display_surface,
                self.game.health_points,
                self.game.remaining_lives,
                self.game.coins,
                self.game.player.energy,
            )
