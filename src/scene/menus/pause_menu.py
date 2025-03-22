from pygame.rect import Rect
from scene.scene import Scene
from resource_manager import ResourceManager
from settings import *
from scene.menus.menu_utils import *


class PauseMenu(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

        X = WINDOW_WIDTH // 2
        Y = WINDOW_HEIGHT // 2
        WIDTH = 200
        HEIGHT = 50

        self.music_bar_y = Y + 100
        self.effects_bar_y = Y + 150

        self.pause_menu_title = Rect(X - 125, Y - 300, WIDTH, HEIGHT)
        self.continue_btn = Rect(X - 100, Y - 100, WIDTH, HEIGHT)
        self.restart_btn = Rect(X - 100, Y, WIDTH, HEIGHT)

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def draw(self, display_surface):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        display_surface.blit(overlay, (0, 0))

        font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

        draw_button(display_surface, self.continue_btn, "Continue", font)
        draw_button(display_surface, self.restart_btn, "Restart", font)

        draw_music_volume_bar(display_surface, self.music_bar_y, font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, font)

    def _mouse_button_down(self, event):
        if self.continue_btn.collidepoint(event.pos):
            self.director.pop_scene()

        elif self.restart_btn.collidepoint(event.pos):
            from game import Game

            self.director.change_scene(Game(self.director))
