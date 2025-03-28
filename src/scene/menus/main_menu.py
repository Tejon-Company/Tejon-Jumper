import pygame

from resource_manager import ResourceManager
from scene.level import Level
from scene.menus.menu import Menu
from scene.menus.menu_utils import (
    check_if_button_was_clicked,
    draw_background,
    draw_button,
)
from scene.menus.settings_menu import SettingsMenu
from scene.scene import Scene
from singletons.settings.resolution_settings import ResolutionSettings


class MainMenu(Menu):
    """
    Gestiona la interfaz del menú principal, incluyendo el título del juego y
    los botones para jugar o acceder a los ajustes. Maneja también las interacciones
    del usuario con estos elementos y la navegación hacia otras escenas del juego.
    """

    def __init__(self):
        super().__init__()
        self._resolution_settings = ResolutionSettings()

        title_font_size = self._resolution_settings.tile_size * 2
        button_font_size = self._resolution_settings.tile_size

        self._title_font = ResourceManager.load_font("backto1982.ttf", title_font_size)
        self._button_font = ResourceManager.load_font(
            "Timetwist-Regular.ttf", button_font_size
        )

        Scene._setup_music("main_menu_music.ogg")

    def _mouse_button_down(self, pos):
        if check_if_button_was_clicked(self._play_button, pos):
            first_level = Level(1)
            self._director.change_scene(first_level)

        elif check_if_button_was_clicked(self._settings_button, pos):
            self._director.push_scene(SettingsMenu())

    def draw(self, display_surface):
        draw_background(display_surface)

        self._draw_title(display_surface)

        self._draw_buttons(display_surface)

    def _draw_title(self, display_surface):
        text_surface, text_rect = self._create_title_text()
        background_surface, background_rect = self._create_title_background(text_rect)

        display_surface.blit(background_surface, background_rect.topleft)
        display_surface.blit(text_surface, text_rect)

    def _create_title_text(self):
        text_surface = self._title_font.render("Tejon jumper", True, "black")
        text_rect = text_surface.get_rect(
            center=(
                self._resolution_settings.window_width // 2,
                self._resolution_settings.window_height // 4,
            )
        )
        return text_surface, text_rect

    def _create_title_background(self, text_rect):
        padding_x = self._resolution_settings.window_width * 0.025
        padding_y = self._resolution_settings.window_height * 0.05
        beige_rect = text_rect.inflate(padding_x, padding_y)
        background_surface = pygame.Surface(
            (beige_rect.width, beige_rect.height), pygame.SRCALPHA
        )
        opacity = 215
        background_surface.fill((245, 245, 220, opacity))
        return background_surface, beige_rect

    def _draw_buttons(self, display_surface):
        button_width = self._resolution_settings.window_width * 0.2
        button_height = self._resolution_settings.window_height * 0.1

        self._play_button = draw_button(
            display_surface,
            "Jugar",
            self._button_font,
            self._resolution_settings.window_height * 0.5,
            width=button_width,
            height=button_height,
        )

        self._settings_button = draw_button(
            display_surface,
            "Ajustes",
            self._button_font,
            self._resolution_settings.window_height * 0.67,
            width=button_width,
            height=button_height,
        )
