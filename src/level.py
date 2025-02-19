from settings import *
from entities.sprite import Sprite
from entities.player import Player


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()

        self._setup(tmx_map)

    def _setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.all_sprites, self.platform_group),
            )

        for object in tmx_map.get_layer_by_name("Objects"):
            if object.name == "Player":
                Player((object.x, object.y), object.image, self.all_sprites)

    def run(self, delta_time):
        self.all_sprites.update(self.platform_group, delta_time)
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
