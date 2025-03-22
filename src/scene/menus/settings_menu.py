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

        X = WINDOW_WIDTH // 2
        Y = WINDOW_HEIGHT // 2
        WIDTH = 200
        HEIGHT = 50
        VOLUME_BAR_HEIGHT = 20

        self.music_volume_bar = Rect(X - WIDTH // 2, Y - 150, WIDTH, VOLUME_BAR_HEIGHT)
        self.effects_volume_bar = Rect(
            X - WIDTH // 2, Y - 100, WIDTH, VOLUME_BAR_HEIGHT
        )

        self.difficulty_btn = Rect(X - WIDTH // 2, Y - 30, WIDTH, HEIGHT)
        self.resolution_btn = Rect(X - WIDTH // 2, Y + 50, WIDTH, HEIGHT)
        self.back_btn = Rect(X - WIDTH // 2, Y + 130, WIDTH, HEIGHT)

        self.music_volume = pygame.mixer.music.get_volume()
        self.effects_volume = ResourceManager.get_effects_volume()

        self.difficulty_levels = ["Easy", "Hard"]
        self.current_difficulty = 1

        self.resolutions = [(800, 600), (1280, 720), (1920, 1080)]
        self.current_resolution = 1

        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", 20)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def _mouse_button_down(self, event):
        if self.difficulty_btn.collidepoint(event.pos):
            self.current_difficulty = (self.current_difficulty + 1) % len(
                self.difficulty_levels
            )

        elif self.back_btn.collidepoint(event.pos):
            from scene.menus.main_menu import MainMenu

            self.director.change_scene(MainMenu(self.director))

    def draw(self, display_surface):
        display_background(display_surface, self.background)

        self.music_volume = draw_volume_bar(
            display_surface,
            self.music_volume_bar,
            self.music_volume,
            "Music",
            self.font,
        )
        self.effects_volume = draw_volume_bar(
            display_surface,
            self.effects_volume_bar,
            self.effects_volume,
            "Sound Effects",
            self.font,
        )

        display_label(
            display_surface,
            "Game Mode",
            self.difficulty_btn.x - 150,
            self.difficulty_btn.y + 15,
            self.font,
        )
        draw_button(
            display_surface,
            self.difficulty_btn,
            f"{self.difficulty_levels[self.current_difficulty]}",
            self.font,
        )

        display_label(
            display_surface,
            "Resolution",
            self.resolution_btn.x - 135,
            self.resolution_btn.y + 15,
            self.font,
        )
        resolution_text = f"{self.resolutions[self.current_resolution][0]}x{self.resolutions[self.current_resolution][1]}"
        draw_button(display_surface, self.resolution_btn, resolution_text, self.font)
        draw_button(display_surface, self.back_btn, "Return", self.font)
