from scene.menus.menu import Menu
from scene.menus.menu_utils import *
from singletons.settings.resolution_settings import ResolutionSettings


class VictoryMenu(Menu):
    """
    Muestra una pantalla de victoria o finalización del juego.
    Proporciona botones para volver al menú principal o salir del juego.
    """

    def __init__(self, boss_has_been_defeated):
        super().__init__()

        self.boss_has_been_defeated = boss_has_been_defeated

        resolution_settings = ResolutionSettings()
        self.background = ResourceManager.load_image("menu_background.jpeg")

        self.message_y = 0.25 * resolution_settings.window_height
        self.message_x = 0.28 * resolution_settings.window_width

        self.replay_button_y = 0.45 * resolution_settings.window_height
        self.quit_button_y = 0.5833 * resolution_settings.window_height

        font_size = int(resolution_settings.tile_size * 0.7)
        self.font = ResourceManager.load_font("Timetwist-Regular.ttf", font_size)

    def _mouse_button_down(self, pos):
        if check_if_button_was_clicked(self.main_menu_button, pos):
            from scene.menus.main_menu import MainMenu

            self.director.change_scene(MainMenu())

        elif check_if_button_was_clicked(self.quit_button, pos):
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
            self.font,
        )
        self._draw_buttons(display_surface)

    def _draw_buttons(self, display_surface):
        self.main_menu_button = draw_button(
            display_surface,
            "Menú principal",
            self.font,
            self.replay_button_y,
        )

        self.quit_button = draw_button(
            display_surface,
            "Cerrar el juego",
            self.font,
            self.quit_button_y,
        )
