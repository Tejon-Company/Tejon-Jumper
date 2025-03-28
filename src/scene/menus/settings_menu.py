from scene.menus.menu import Menu
from scene.menus.menu_utils import *
from singletons.settings.difficulty_settings import DifficultySettings
from singletons.settings.resolution_settings import ResolutionSettings


class SettingsMenu(Menu):
    """
    Responsable de mostrar y gestionar las opciones de configuración
    como el volumen de la música y efectos, la dificultad del juego y la resolución
    de pantalla. Permite al usuario modificar estos ajustes y volver al menú principal.
    """

    def __init__(self):
        super().__init__()
        self._background = ResourceManager.load_image("menu_background.jpeg")

        self._resolution_settings = ResolutionSettings()
        self._difficulty_settings = DifficultySettings()

        self._music_bar_y = self._resolution_settings.window_height * 0.35
        self._effects_bar_y = self._resolution_settings.window_height * 0.45

        self._difficulty_btn_y = self._resolution_settings.window_height * 0.55
        self._resolution_btn_y = self._resolution_settings.window_height * 0.65
        self._return_btn_y = self._resolution_settings.window_height * 0.75

        font_size = int(self._resolution_settings.tile_size * 0.7)
        self._font = ResourceManager.load_font("Timetwist-Regular.ttf", font_size)

    def _mouse_button_down(self, pos):
        if check_if_button_was_clicked(self._return_button, pos):
            self._director.change_scene(SettingsMenu())

        elif check_if_button_was_clicked(self._resolution_button, pos):
            self._director.update_display_surface_resolution()
            self._resolution_settings.update_resolution()
            from scene.menus.main_menu import MainMenu

            self._director.change_scene(MainMenu())

        elif check_if_button_was_clicked(self._difficulty_button, pos):
            self._difficulty_settings.update_difficulty()

    def draw(self, display_surface):
        draw_background(display_surface, self._background)
        self._display_surface = display_surface

        draw_music_volume_bar(display_surface, self._music_bar_y, self._font)
        draw_effects_volume_bar(display_surface, self._effects_bar_y, self._font)

        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self._difficulty_button = draw_button_with_label(
            display_surface,
            self._difficulty_settings.name,
            "Dificultad",
            self._font,
            self._difficulty_btn_y + self._resolution_settings.window_height * 0.02,
        )

        self._resolution_button = draw_button_with_label(
            display_surface,
            f"{self._resolution_settings.window_width}x{self._resolution_settings.window_height}",
            "Resolución",
            self._font,
            self._resolution_btn_y,
        )

        self._return_button = draw_button(
            display_surface,
            "Volver",
            self._font,
            self._return_btn_y,
        )
