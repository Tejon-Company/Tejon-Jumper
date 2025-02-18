from settings import *
from sprites import Sprite, Background
from player import Player
from os.path import join

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for i in range(4):
            Background(
                join("assets", "maps", "background", f"{i}.png"),
                (0, 0), 
                self.all_sprites
            )

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
        self.all_sprites.update(delta_time)
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
