from resource_manager import ResourceManager
from scene.menus.settings_menu import SettingsMenu
from settings import *
import pygame
from scene.menus.menu_utils import draw_button, draw_background
from scene.menus.menu import Menu


class MainMenu(Menu):
    def __init__(self, director):
        super().__init__(director)

        self.background = ResourceManager.load_image("menu_background.jpeg")

        self.title_font = ResourceManager.load_font("backto1982.ttf", 84)

        self.button_font = ResourceManager.load_font("Timetwist-Regular.ttf", 30)

    def _mouse_button_down(self, event):
        if self.play_button.collidepoint(event.pos):
            from game import Game

            self.director.change_scene(Game(self.director))

        elif self.settings_button.collidepoint(event.pos):
            self.director.stack_scene(SettingsMenu(self.director))

    def draw(self, display_surface):
        draw_background(display_surface, self.background)
        self._draw_title(display_surface)
        self._draw_buttons(display_surface)

    def _draw_title(self, display_surface):
        text_surface = self.title_font.render("Tejon jumper", True, "black")
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        )
        beige_rect = text_rect.inflate(20, 20)
        translucent_surface = pygame.Surface(
            (beige_rect.width, beige_rect.height), pygame.SRCALPHA
        )
        opacity = 215
        translucent_surface.fill((245, 245, 220, opacity))
        display_surface.blit(translucent_surface, beige_rect.topleft)
        display_surface.blit(text_surface, text_rect)

    def _draw_buttons(self, display_surface):
        self.play_button = draw_button(
            display_surface,
            "Play",
            self.button_font,
            WINDOW_HEIGHT // 2,
            width=230,
            height=70,
        )

        self.settings_button = draw_button(
            display_surface,
            "Settings",
            self.button_font,
            WINDOW_HEIGHT // 2 + 120,
            width=230,
            height=70,
        )
