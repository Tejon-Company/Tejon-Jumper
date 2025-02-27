from settings import *
from characters.sprite import Sprite
from characters.players.player import Player
from characters.players.player_state import PlayerState
from pygame.sprite import Group, spritecollide
from characters.enemies.enemy_factory import enemy_factory
from scene.background import Background
from scene.camera import Camera
from os.path import join
from berries.berrie_factory import berrie_factory
from pygame.mixer import music
from scene.scene import Scene
from pytmx.util_pygame import load_pygame
import os


class Level(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()
        self.tmx_map = load_pygame(
            join("assets", "maps", "levels",  "level0.tmx"))
        self.background_folder = join(
            "assets", "maps", "backgrounds", "background1")
        self.music_file = join("assets", "sounds", "music", "level_1.ogg")

        self._init_groups()
        self._init_camera()

        self._setup_background()
        self._setup_music()
        self._setup_terrain()
        self._setup_characters()
        self._setup_berries()

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

    def _init_camera(self):
        map_width = self.tmx_map.width * TILE_SIZE
        map_height = self.tmx_map.height * TILE_SIZE
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

    def _setup_terrain(self):
        for x, y, surf in self.tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["all_sprites"], self.groups["platforms"]),
            )

    def _setup_characters(self):
        for character in self.tmx_map.get_layer_by_name("Objects"):
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

    def _setup_berries(self):
        for berrie in self.tmx_map.get_layer_by_name("Berries"):
            berrie_factory(berrie, self.groups)

    def _check_collision(self):
        collisions = tuple(
            spritecollide(self.player, self.groups[group], False)
            for group in ["hedgehogs", "squirrels", "foxes", "projectiles", "bats"]
        )

        if all(len(c) == 0 for c in collisions):
            return

        for group, collision_list in zip(["hedgehogs", "squirrels", "foxes", "projectiles", "bats"], collisions):
            for enemy in collision_list:
                self._handle_collision(enemy, group)

    def _handle_collision(self, enemy, group):
        # Determinar la dirección de la colisión
        direction = self._get_collision_direction(self.player, enemy)

        # Mostrar la información por pantalla
        self._display_collision_info(enemy, group, direction)

        # Aplicar daño al jugador
        player_state = self.player.receive_damage()

        match player_state:
            case PlayerState.ALIVE:
                pass
            case PlayerState.DAMAGED:
                print(self.player.health_points)
                pass
            case PlayerState.DEAD:
                pass
            case PlayerState.GAME_OVER:
                pass

    def _get_collision_direction(self, player, enemy):
        # Calcular la diferencia de posición entre el jugador y el enemigo
        dx = player.rect.centerx - enemy.rect.centerx
        dy = player.rect.centery - enemy.rect.centery

        if abs(dx) > abs(dy):
            return "izquierda" if dx > 0 else "derecha"
        else:
            return "arriba" if dy > 0 else "abajo"

    def _display_collision_info(self, enemy, group, direction):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Colisión con {group} por {direction}", True, (255, 255, 255))
        self.display_surface.blit(text, (700, 10))


    def update(self, delta_time):
        platform_rects = [
            platform.rect for platform in self.groups["platforms"]]
        self.groups["all_sprites"].update(platform_rects, delta_time)
        self.groups["berries"].update(self.player)

        self.camera.update(self.player)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()

    def draw(self, display_surface):
        self.camera.draw_background(
            self.groups["backgrounds"], display_surface)

        for sprite in self.groups["all_sprites"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["berries"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))
        self._check_collision()
