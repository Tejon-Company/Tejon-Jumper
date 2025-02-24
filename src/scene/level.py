from settings import *
from characters.sprite import Sprite
from characters.players.player import Player
from characters.enemies.moving_enemies.hedgehog import Hedgehog
from characters.enemies.moving_enemies.fox import Fox
from pygame.sprite import Group
from characters.enemies.enemy_factory import enemy_factory
from scene.background import Background
from scene.camera import Camera
from os.path import join
import os


class Level:
    def __init__(self, tmx_map, background):
        self.display_surface = pygame.display.get_surface()
        self.background_folder = join("assets", "maps", "backgrounds", background)

        self._init_groups()
        self._init_camera(tmx_map)

        self._setup_background(tmx_map)
        self._setup_terrain(tmx_map)
        self._setup_characters(tmx_map)

    def _init_groups(self):
        self.groups = {
            "all_sprites": Group(),
            "platforms": Group(),
            "hedgehogs": Group(),
            "foxes": Group(),
            "backgrounds": Group(),
        }

        self.player = None

    def _init_camera(self, tmx_map):
        map_width = tmx_map.width * TILE_SIZE
        map_height = tmx_map.height * TILE_SIZE
        self.camera = Camera(map_width, map_height)

    def _setup_background(self, tmx_map):
        image_files = self._get_image_files()
        map_width = tmx_map.width * TILE_SIZE

        for i, image_name in enumerate(image_files):
            Background(
                join(self.background_folder, image_name),
                (0, 0),
                BACKGROUND_SPEEDS[i % len(BACKGROUND_SPEEDS)],
                PARALLAX_FACTOR[i % len(PARALLAX_FACTOR)],
                map_width,
                self.groups["backgrounds"],
            )

    def _get_image_files(self):
        image_files = []
        for file in os.listdir(self.background_folder):
            if file.endswith(".png"):
                image_files.append(file)

        image_files.sort(key=lambda file_name: int(file_name.split(".")[0]))

        return image_files

    def _setup_terrain(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["all_sprites"], self.groups["platforms"]),
            )

    def _setup_characters(self, tmx_map):
        for character in tmx_map.get_layer_by_name("Objects"):
            if character.name == "Player":
                self._setup_player(character)
            else:
                enemy_factory(character, self.groups)

    def _setup_player(self, character):
        assert not self.player, "Only one player is allowed"

        self.player = Player(
            (character.x, character.y),
            pygame.Surface((32, 32)),
            self.groups["all_sprites"],
        )

    def run(self, delta_time):
        platform_rects = [platform.rect for platform in self.groups["platforms"]]
        self.groups["all_sprites"].update(platform_rects, delta_time)

        self.camera.update(self.player)
        self.camera.update_background(self.groups["backgrounds"], delta_time)
        self.camera.draw_background(self.groups["backgrounds"], self.display_surface)

        for sprite in self.groups["all_sprites"]:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
