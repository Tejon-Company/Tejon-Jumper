from settings import *
from entities.sprite import Sprite
from entities.players.player import Player
from entities.enemies.moving_enemies.hedgehog import Hedgehog
from pygame.sprite import Group
from entities.entitie_factory import entitie_factory


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        self.groups = {
            "all_sprites": Group(),
            "platforms": Group(),
            "hedgehogs": Group(),
        }

        self._setup(tmx_map)

    def _setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["all_sprites"], self.groups["platforms"]),
            )

        for object in tmx_map.get_layer_by_name("Objects"):
            entitie_factory(object, self.groups)

    def run(self, delta_time):
        platform_rects = [platform.rect for platform in self.groups["platforms"]]

        self.groups["all_sprites"].update(platform_rects, delta_time)
        self.display_surface.fill("black")
        self.groups["all_sprites"].draw(self.display_surface)
