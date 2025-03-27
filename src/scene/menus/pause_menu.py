from scene.menus.menu import Menu
from scene.menus.menu_utils import *
from singletons.settings.resolution_settings import ResolutionSettings
from singletons.director import Director
from singletons.game import Game


class PauseMenu(Menu):
    def __init__(self):
        super().__init__()

        self.director = Director()

        resolution_settings = ResolutionSettings()

        self.music_bar_y = 0.25 * resolution_settings.window_height
        self.effects_bar_y = 0.3333 * resolution_settings.window_height
        self.continue_button_y = 0.45 * resolution_settings.window_height
        self.restart_button_y = 0.5833 * resolution_settings.window_height

        font_size = int(resolution_settings.tile_size * 0.7)
        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", font_size)

    def _handle_event(self, event):
        super()._handle_event(event)
        keys = pygame.key.get_just_released()

        if keys[pygame.K_p]:
            self._exit_pause()

    def _exit_pause(self):
        self.click_button_sound.play()
        game = Game()
        game.reload_game()
        from scene.level import Level

        self.director.push_scene(Level(1))

    def _mouse_button_down(self, pos):
        if check_if_button_was_clicked(self.continue_button, pos):
            self.director.pop_scene()

        elif check_if_button_was_clicked(self.restart_button, pos):
            self._exit_pause()

    def draw(self, display_surface):
        draw_music_volume_bar(display_surface, self.music_bar_y, self.font)
        draw_effects_volume_bar(display_surface, self.effects_bar_y, self.font)

        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self.continue_button = draw_button(
            display_surface,
            "Continuar",
            self.font,
            self.continue_button_y,
        )

        self.restart_button = draw_button(
            display_surface,
            "Reiniciar partida",
            self.font,
            self.restart_button_y,
        )
