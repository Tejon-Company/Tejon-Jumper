from settings import *
from characters.sprite import Sprite
from characters.players.player import Player
from characters.players.player_state import PlayerState
from pygame.sprite import Group, spritecollide
from characters.enemies.enemy_factory import enemy_factory
from scene.background import Background
from scene.camera import Camera
from ui.ui import UI
from os.path import join
from berries.berrie_factory import berrie_factory
from pygame.mixer import music
import os


class Level:
    def __init__(self, tmx_map, background, music):
        self.display_surface = pygame.display.get_surface()
        self.background_folder = join(
            "assets", "maps", "backgrounds", background)
        self.music_file = join("assets", "sounds", "music", music)

        self.player = None  
        self.ui = None

        self._init_groups()
        self._init_camera(tmx_map)

        self._setup_background()
        self._setup_music()
        self._setup_terrain(tmx_map)
        self._setup_characters(tmx_map)
        self._setup_berries(tmx_map)

        if self.player:
            self.ui = UI(self.display_surface, self.player)

    def _init_groups(self):
        self.groups = {
            "all_sprites": Group(),
            "platforms": Group(),
            "hedgehogs": Group(),
            "mushrooms": Group(),
            "squirrels": Group(),
            "foxes": Group(),
            "backgrounds": [],
            "projectiles": Group(),
            "berries": Group(),
            "bats": Group()
        }

        self.player = None

    def _init_camera(self, tmx_map):
        map_width = tmx_map.width * TILE_SIZE
        map_height = tmx_map.height * TILE_SIZE
        self.camera = Camera(map_width, map_height)

    def _setup_background(self):
        image_files = self._get_image_files()

        for i, image_name in enumerate(image_files):
            Background(
                join(self.background_folder, image_name),
                (0, 0),
                PARALLAX_FACTOR[i % len(PARALLAX_FACTOR)],
                self.groups["backgrounds"],
            )

    def _get_image_files(self,):
        image_files = []
        for file in os.listdir(self.background_folder):
            if file.endswith(".png"):
                image_files.append(file)

        image_files.sort(key=lambda file_name: int(file_name.split(".")[0]))

        return image_files

    def _setup_music(self):
        music.load(self.music_file)
        music.play(-1)

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
            lives=3 if DIFFICULTY == Difficulty.NORMAL else 1,
            health_points=5 if DIFFICULTY == Difficulty.NORMAL else 3
        )

    def _setup_berries(self, tmx_map):
        for berrie in tmx_map.get_layer_by_name("Berries"):
            berrie_factory(berrie, self.groups)

    def run(self, delta_time):
        platform_rects = [
            platform.rect for platform in self.groups["platforms"]]
        self.groups["all_sprites"].update(platform_rects, delta_time)
        self.groups["berries"].update(self.player)

        self.camera.update(self.player)
        self.camera.draw_background(
            self.groups["backgrounds"], self.display_surface)

        for sprite in self.groups["all_sprites"]:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["berries"]:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))

        if self.ui:
            self.ui.draw_hearts() 

        self._check_collision()

    def _check_collision(self):
        collisions = tuple(
            spritecollide(self.player, self.groups[group], False)
            for group in ["hedgehogs", "squirrels", "foxes", "projectiles", "bats"]
        )

        if all(len(c) == 0 for c in collisions):
            return

        player_state = self.player.receive_damage()

        match player_state:
            case PlayerState.ALIVE:
                pass
            case PlayerState.DAMAGED:
                print(self.player.health_points)
                if self.ui:  
                    self.ui.draw_hearts()
                pass
            case PlayerState.DEAD:
                pass
            case PlayerState.GAME_OVER:
                pass
