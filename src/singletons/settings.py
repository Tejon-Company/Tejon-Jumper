from singletons.singleton_meta import SingletonMeta
from enum import Enum, auto


class Settings(metaclass=SingletonMeta):
    class Difficulty(Enum):
        EASY = auto()
        HARD = auto()

    window_width, window_height = 1280, 720

    tile_size = 32
    animation_speed = 6
    parallax_factor = [0.1, 0.2, 0.4, 0.9]

    difficulty = Difficulty.EASY

    levels_config = {
        1: {
            "background": "background1",
            "music": "level_1.ogg",
            "map": "level1.tmx",
        },
        2: {
            "background": "background2",
            "music": "level_2.ogg",
            "map": "level2.tmx",
        },
        3: {
            "background": "background3",
            "music": "level_3.ogg",
            "map": "level3.tmx",
        },
    }

    def change_difficulty(self):
        if self.difficulty == self.Difficulty.EASY:
            self.difficulty = self.Difficulty.HARD
        else:
            self.difficulty = self.Difficulty.EASY

    def change_resolution(self):
        if self.window_width == 1280 and self.window_height == 720:
            self.window_width, self.window_height = 1920, 1080
            self.tile_size = 48
        else:
            self.window_width, self.window_height = 1280, 720
            self.tile_size = 32
