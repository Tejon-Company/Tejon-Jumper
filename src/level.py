from settings import *
from entities.sprite import Sprite
from entities.players.player import Player
from entities.enemies.moving_enemies.hedgehog import Hedgehog
from pygame.sprite import Group
from entities.entitie_factory import entitie_factory
from background import Background
from camera import Camera
from os.path import join
import os


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        self.groups = {
            "all_sprites": Group(),
            "platforms": Group(),
            "hedgehogs": Group(),
            "backgrounds": Group()
        }

        map_width = tmx_map.width * TILE_SIZE
        map_height = tmx_map.height * TILE_SIZE

        self.camera = Camera(map_width, map_height)

        self._setup(tmx_map)


    def _setup(self, tmx_map):
        background_folder = join("assets", "maps", "background", "background1")

        image_files = [
            file for file in os.listdir(background_folder) if file.endswith(".png")
        ]
        image_files.sort(key=lambda file_name: int(file_name.split(".")[0]))

        for image_name in image_files:
            Background(join(background_folder, image_name), (0, 0), self.groups["backgrounds"])

        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["all_sprites"], self.groups["platforms"]),
            )

        for object in tmx_map.get_layer_by_name("Objects"):
            if object.name == "Player":
                self.player = Player((object.x, object.y), pygame.Surface((32, 32)), self.groups["all_sprites"])

            entitie_factory(object, self.groups)

            
    def run(self, delta_time):
        platform_rects = [platform.rect for platform in self.groups["platforms"]]
        self.groups["all_sprites"].update(platform_rects, delta_time)

        self.camera.update(self.player)

        self.groups["backgrounds"].draw(self.display_surface)

        for sprite in self.groups["all_sprites"]:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
    