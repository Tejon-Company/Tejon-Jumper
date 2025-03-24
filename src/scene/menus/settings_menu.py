from resource_manager import ResourceManager
from settings import *
from scene.menus.menu_utils import *
from resource_manager import ResourceManager
from scene.menus.menu import Menu


class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.background = ResourceManager.load_image("menu_background.jpeg")

        self.music_bar_y = WINDOW_HEIGHT * 0.35
        self.effects_bar_y = WINDOW_HEIGHT * 0.45

        self.difficulty_btn_y = WINDOW_HEIGHT * 0.55
        self.resolution_btn_y = WINDOW_HEIGHT * 0.65
        self.return_btn_y = WINDOW_HEIGHT * 0.75

        self.difficulties = ["Easy", "Hard"]
        self.current_difficulty = 1

        self.resolutions = [(1280, 720), (1920, 1080)]
        self.current_resolution = 0

        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

    def _mouse_button_down(self, event):
        if self.return_button.collidepoint(event.pos):
            self.click_button_sound.play()
            self.director.pop_scene()

        elif self.resolution_button.collidepoint(event.pos):
            self.click_button_sound.play()
            self.current_resolution = (self.current_resolution + 1) % len(
                self.resolutions
            )

        elif self.difficulty_button.collidepoint(event.pos):
            self.click_button_sound.play()
            self.current_difficulty = (self.current_difficulty + 1) % len(
                self.difficulties
            )

    def draw(self, display_surface):
        draw_background(display_surface, self.background)

        draw_music_volume_bar(display_surface, self.music_bar_y, self.font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, self.font)

        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self.difficulty_button = draw_button_with_label(
            display_surface,
            f"{self.difficulties[self.current_difficulty]}",
            "Game Mode",
            self.font,
            self.difficulty_btn_y + WINDOW_HEIGHT * 0.02,
        )

        current_resolution = self.resolutions[self.current_resolution]
        width, height = current_resolution

        self.resolution_button = draw_button_with_label(
            display_surface,
            f"{width}x{height}",
            "Resolution",
            self.font,
            self.resolution_btn_y,
        )

        self.return_button = draw_button(
            display_surface,
            "Return",
            self.font,
            self.return_btn_y,
        )
