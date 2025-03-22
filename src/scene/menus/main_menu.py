from scene.scene import Scene
from resource_manager import ResourceManager
from scene.menus.settings_menu import SettingsMenu
from settings import *
import pygame
from scene.menus.menu_utils import draw_button, display_background


class MainMenu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.display_surface = pygame.display.get_surface()
        self.background = ResourceManager.load_image("menu_background.jpeg")

        self.title_font = ResourceManager.load_font("backto1982.ttf", 84)
        self.button_font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)
        self.button_font.set_bold(True)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def _mouse_button_down(self, event):
        if self.play_button.collidepoint(event.pos):
            from game import Game

            self.director.change_scene(Game(self.director))

        elif self.settings_button.collidepoint(event.pos):
            self.director.stack_scene(SettingsMenu(self.director))

    def draw(self, display_surface):
        display_background(display_surface, self.background)

        self._draw_title(display_surface)

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
