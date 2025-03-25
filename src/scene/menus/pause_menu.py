from scene.menus.menu import Menu
from scene.menus.menu_utils import *
from singletons.settings import Settings
from singletons.director import Director
from singletons.game import Game


class PauseMenu(Menu):
    def __init__(self):
        super().__init__()

        settings = Settings()

        self.music_bar_y = 0.25 * settings.window_height
        self.effects_bar_y = 0.3333 * settings.window_height
        self.continue_button_y = 0.45 * settings.window_height
        self.restart_button_y = 0.5833 * settings.window_height

        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

    def _mouse_button_down(self, event):
        director = Director()

        if self.continue_button.collidepoint(event.pos):
            self.click_button_sound.play()
            director.pop_scene()

        elif self.restart_button.collidepoint(event.pos):
            self.click_button_sound.play()
            game = Game()
            game.reload_game()
            from scene.level import Level
            director.push_scene(Level(1))

    def draw(self, display_surface):
        draw_music_volume_bar(display_surface, self.music_bar_y, self.font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, self.font)

        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
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
