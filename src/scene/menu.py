from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from scene.scene import Scene
from resource_manager import ResourceManager
from scene.settings_menu import SettingsMenu
from settings import *
import pygame


class Menu(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

        X = WINDOW_WIDTH // 2
        Y = WINDOW_HEIGHT // 2
        WIDTH = 230
        HEIGHT = 70

        self.logo = ResourceManager.load_image("logo.png")
        self.logo_rect = self.logo.get_rect(center=(X, Y - 150))

        self.play_btn = Rect(X - WIDTH // 2, Y, WIDTH, HEIGHT)
        self.settings_btn = Rect(X - WIDTH // 2, Y + 120, WIDTH, HEIGHT)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def _mouse_button_down(self, event):
        if self.play_btn.collidepoint(event.pos):
            from game import Game

            self.director.change_scene(Game(self.director))

        if self.settings_btn.collidepoint(event.pos):
            self.director.change_scene(SettingsMenu(self.director))

    def draw(self, display_surface):
        display_surface.fill((34, 139, 34))
        display_surface.blit(self.logo, self.logo_rect.topleft)

        font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

        self._draw_button(display_surface, self.play_btn, "Play", font)
        self._draw_button(display_surface, self.settings_btn, " Settings", font)

    def _draw_button(self, display_surface, rect, text, font):
        draw_rect(display_surface, "black", rect)
        text_surf = font.render(text, True, "white")
        text_rect = text_surf.get_rect(center=rect.center)
        display_surface.blit(text_surf, text_rect.topleft)

    def run(self):
        if len(self.stack) == 0:
            self.stack.append(Menu(self))

        while len(self.stack) > 0:
            scene = self.stack[-1]
            self._loop(scene)
