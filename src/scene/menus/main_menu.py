from resource_manager import ResourceManager
from scene.menus.settings_menu import SettingsMenu
import pygame
from scene.menus.menu_utils import draw_button, draw_background
from scene.menus.menu import Menu
from scene.level import Level
from scene.scene import Scene
from singletons.settings import Settings


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self.background = ResourceManager.load_image("menu_background.jpeg")

        self.title_font = ResourceManager.load_font("backto1982.ttf", 84)
        self.button_font = ResourceManager.load_font("Timetwist-Regular.ttf", 30)

        Scene._setup_music("main_menu_music.ogg")

    def _mouse_button_down(self, event):
        if self.play_button.collidepoint(event.pos):
            self.click_button_sound.play()

            first_level = Level(1)
            self.director.change_scene(first_level)

        elif self.settings_button.collidepoint(event.pos):
            self.click_button_sound.play()
            self.director.push_scene(SettingsMenu())

    def draw(self, display_surface):
        draw_background(display_surface, self.background)

        self._draw_title(display_surface)

        self._draw_buttons(display_surface)

    def _draw_title(self, display_surface):
        text_surface, text_rect = self._create_title_text()
        background_surface, background_rect = self._create_title_background(text_rect)

        display_surface.blit(background_surface, background_rect.topleft)
        display_surface.blit(text_surface, text_rect)

    def _create_title_text(self):
        text_surface = self.title_font.render("Tejon jumper", True, "black")
        text_rect = text_surface.get_rect(
            center=(self.settings.window_width // 2, self.settings.window_height // 4)
        )
        return text_surface, text_rect

    def _create_title_background(self, text_rect):
        padding_x = self.settings.window_width * 0.025
        padding_y = self.settings.window_height * 0.05
        beige_rect = text_rect.inflate(padding_x, padding_y)
        background_surface = pygame.Surface(
            (beige_rect.width, beige_rect.height), pygame.SRCALPHA
        )
        opacity = 215
        background_surface.fill((245, 245, 220, opacity))
        return background_surface, beige_rect

    def _draw_buttons(self, display_surface):
        button_width = self.settings.window_width * 0.2
        button_height = self.settings.window_height * 0.1

        self.play_button = draw_button(
            display_surface,
            "Play",
            self.button_font,
            self.settings.window_height * 0.5,
            width=button_width,
            height=button_height,
        )

        self.settings_button = draw_button(
            display_surface,
            "Settings",
            self.button_font,
            self.settings.window_height * 0.67,
            width=button_width,
            height=button_height,
        )
