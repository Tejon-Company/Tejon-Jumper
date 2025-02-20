from settings import *
from sprites import Sprite
from background import Background
from player import Player
from os.path import join
import os


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        background_folder = join("assets", "maps", "background", "background1")

        image_files = [
            file for file in os.listdir(background_folder) if file.endswith(".png")
        ]
        image_files.sort(key=lambda file_name: int(file_name.split(".")[0]))

        for image_name in image_files:
            Background(join(background_folder, image_name), (0, 0), self.backgrounds)

        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.all_sprites, self.collision_sprites),
            )

        for object in tmx_map.get_layer_by_name("Objects"):
            if object.name == "Player":
                Player((object.x, object.y), self.all_sprites, self.collision_sprites)

    def run(self, delta_time):
        self.backgrounds.draw(self.display_surface)

        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.display_surface)
