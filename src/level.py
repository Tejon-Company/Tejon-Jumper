from settings import *
from sprites import Sprite
from player import Player
from camera import Camera


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        map_width = tmx_map.width * TILE_SIZE
        map_height = tmx_map.height * TILE_SIZE

        self.camera = Camera(map_width, map_height)

        self._setup(tmx_map)


    def _setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.all_sprites, self.collision_sprites),
            )

        for object in tmx_map.get_layer_by_name("Objects"):
            if object.name == "Player":
                self.player = Player((object.x, object.y), self.all_sprites, self.collision_sprites)

    def run(self, delta_time):
        self.all_sprites.update(delta_time)
        self.camera.update(self.player)
        self.display_surface.fill("black")

        # self.all_sprites.draw(self.display_surface)

        for sprite in self.all_sprites:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))

