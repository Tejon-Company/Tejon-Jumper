from pygame.rect import Rect
from scene.scene import Scene
from resource_manager import ResourceManager
from settings import *
import pygame
from scene.menus.menu_utils import *


class SettingsMenu(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()
        self.background = ResourceManager.load_image("menu_background.jpeg")

        Y = WINDOW_HEIGHT // 2

        self.music_bar_y = Y - 150
        self.effects_bar_y = Y - 100

        self.difficulty_btn_y = Y - 30
        self.resolution_btn_y = Y + 50
        self.return_btn_y = Y + 130

        self.difficulties = ["Easy", "Hard"]
        self.current_difficulty = 1

        self.resolutions = [(1280, 720), (1920, 1080)]
        self.current_resolution = 0

        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", 20)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def _mouse_button_down(self, event):
        if self.return_button.collidepoint(event.pos):
            self.director.pop_scene()

        elif self.resolution_button.collidepoint(event.pos):
            self.current_resolution = (self.current_resolution + 1) % len(
                self.resolutions
            )

        elif self.difficulty_button.collidepoint(event.pos):
            self.current_difficulty = (self.current_difficulty + 1) % len(
                self.difficulties
            )

    def draw(self, display_surface):
        display_background(display_surface, self.background)

        draw_music_volume_bar(display_surface, self.music_bar_y, self.font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, self.font)

        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self.difficulty_button = draw_button_with_label(
            display_surface,
            f"{self.difficulties[self.current_difficulty]}",
            "Game Mode",
            self.font,
            self.difficulty_btn_y + 15,
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
