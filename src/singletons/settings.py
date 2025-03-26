from singletons.singleton_meta import SingletonMeta


class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self._resolutions = (
            {
                "name": "hd",
                "window_width": 1280,
                "window_height": 720,
                "tile_size": 32,
            },
            {
                "name": "full_hd",
                "window_width": 1920,
                "window_height": 1050,
                "tile_size": 48,
            },
        )

        self._current_resolution_index = 0

        self.levels_config = {
            1: {
                "background": "background1",
                "music": "level_1.ogg",
                "map": "level1.tmx",
                "map_size": 121,
            },
            2: {
                "background": "background2",
                "music": "level_2.ogg",
                "map": "level2.tmx",
                "map_size": 154,
            },
            3: {
                "background": "background3",
                "music": "level_3.ogg",
                "map": "level3.tmx",
                "map_size": 113,
            },
        }

        self._difficulties = (
            {
                "name": "Fácil",
                "player_health_points": 5,
                "player_lives": 3,
                "bear_health_points": 3,
            },
            {
                "name": "Difícil",
                "player_health_points": 3,
                "player_lives": 1,
                "bear_health_points": 5,
            },
        )

        self._current_difficulty = 0

    def get_resolution_name(self):
        return self._resolutions[self._current_resolution_index]["name"]

    def get_window_height(self):
        return self._resolutions[self._current_resolution_index]["window_height"]

    def get_window_width(self):
        return self._resolutions[self._current_resolution_index]["window_width"]

    def get_tile_size(self):
        return self._resolutions[self._current_resolution_index]["tile_size"]

    def update_resolution(self):
        self._current_resolution_index = self._current_resolution_index + 1 % len(
            self._resolutions
        )

    def get_difficulty(self):
        return self._difficulties[self._current_difficulty]["name"]

    def update_difficulty(self):
        self._current_difficulty = self._current_difficulty + 1 % len(
            self._difficulties
        )

    def get_player_health_points(self):
        return self._difficulties[self._current_difficulty][
            "player_health_points"
        ]

    def get_player_lives(self):
        return self._difficulties[self._current_difficulty]["player_lives"]

    def get_bear_health_points(self):
        return self._difficulties[self._current_difficulty]["bear_health_points"]

    def get_number_of_levels(self):
        return len(self.levels_config)
