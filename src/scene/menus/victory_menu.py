from scene.menus.menu_utils import *
from scene.menus.menu import Menu
from singletons.settings import Settings


class VictoryMenu(Menu):
    def __init__(self, boss_has_been_defeated):
        super().__init__()
        self.boss_has_been_defeated = boss_has_been_defeated
        settings = Settings()
        self.background = ResourceManager.load_image("menu_background.jpeg")
        self.message_y = 0.25 * settings.window_height
        self.message_x = 0.28 * settings.window_width
        self.message_font = ResourceManager.load_font("Timetwist-Regular.ttf", 30)
        self.button_font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)
        self.replay_button_y = 0.45 * settings.window_height
        self.quit_button_y = 0.5833 * settings.window_height

    def _mouse_button_down(self, event):
        if self.replay_button.collidepoint(event.pos):
            from scene.menus.main_menu import MainMenu
            self.director.change_scene(MainMenu())

        elif self.quit_button.collidepoint(event.pos):
            self.director.exit_program()

    def draw(self, display_surface):
        draw_background(display_surface, self.background)
        if self.boss_has_been_defeated:
            victory_message = "¡Felicidades, lograste vencer al oso!"
        else:
            victory_message = (
                "Has finalizado el juego, pero no\nhas sido capaz de derrotar al oso..."
            )

        display_label(
            display_surface,
            victory_message,
            self.message_x,
            self.message_y,
            self.message_font,
        )
        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self.replay_button = draw_button(
            display_surface,
            "Menú principal",
            self.button_font,
            self.replay_button_y,
        )

        self.quit_button = draw_button(
            display_surface,
            "Cerrar el juego",
            self.button_font,
            self.quit_button_y,
        )
