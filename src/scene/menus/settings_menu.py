from scene.menus.menu import Menu
from scene.menus.menu_utils import *
from singletons.settings.resolution_settings import ResolutionSettings
from singletons.settings.difficulty_settings import DifficultySettings


class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.background = ResourceManager.load_image("menu_background.jpeg")

        self.resolution_settings = ResolutionSettings()
        self.difficulty_settings = DifficultySettings()

        self.music_bar_y = self.resolution_settings.window_height * 0.35
        self.effects_bar_y = self.resolution_settings.window_height * 0.45

        self.difficulty_btn_y = self.resolution_settings.window_height * 0.55
        self.resolution_btn_y = self.resolution_settings.window_height * 0.65
        self.return_btn_y = self.resolution_settings.window_height * 0.75

        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

    def _mouse_button_down(self, pos):
        if check_if_button_was_clicked(self.return_button, pos):
            self.director.pop_scene()

        elif check_if_button_was_clicked(self.resolution_button, pos):
            self.current_resolution = (self.current_resolution + 1) % len(
                self.resolutions
            )

        elif check_if_button_was_clicked(self.difficulty_button, pos):
            self.difficulty_settings.update_difficulty()

    def draw(self, display_surface):
        draw_background(display_surface, self.background)

        draw_music_volume_bar(display_surface, self.music_bar_y, self.font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, self.font)

        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self.difficulty_button = draw_button_with_label(
            display_surface,
            self.difficulty_settings.name,
            "Dificultad",
            self.font,
            self.difficulty_btn_y + self.difficulty_settings.window_height * 0.02,
        )

        self.resolution_button = draw_button_with_label(
            display_surface,
            f"{self.resolution_settings.window_width}x{self.resolution_settings.window_height}",
            "Resolución",
            self.font,
            self.resolution_btn_y,
        )

        self.return_button = draw_button(
            display_surface,
            "Volver",
            self.font,
            self.return_btn_y,
        )
