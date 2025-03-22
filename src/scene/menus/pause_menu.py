from scene.scene import Scene
from resource_manager import ResourceManager
from settings import *
from scene.menus.menu_utils import *


class PauseMenu(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

        Y = WINDOW_HEIGHT // 2

        self.music_bar_y = Y - 150
        self.effects_bar_y = Y - 100
        self.continue_button_y = Y - 30
        self.restart_button_y = Y + 50

        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def draw(self, display_surface):
        self._draw_overlay(display_surface)

        self.continue_button = draw_button(
            display_surface,
            "Continue",
            self.font,
            self.continue_button_y,
        )

        self.restart_button = draw_button(
            display_surface,
            "Restart",
            self.font,
            self.restart_button_y,
        )

        draw_music_volume_bar(display_surface, self.music_bar_y, self.font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, self.font)

    def _draw_overlay(self, display_surface):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        display_surface.blit(overlay, (0, 0))

    def _mouse_button_down(self, event):
        if self.continue_button.collidepoint(event.pos):
            self.director.pop_scene()

        elif self.restart_button.collidepoint(event.pos):
            from game import Game

            self.director.change_scene(Game(self.director))
