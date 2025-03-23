from settings import *
from scene.menus.menu_utils import *
from scene.menus.menu import Menu


class Victory(Menu):
    def __init__(self, director):
        super().__init__(director)
        self.background = ResourceManager.load_image("menu_background.jpeg")
        self.message_y=0.35 * WINDOW_HEIGHT
        self.message_x=0.28 * WINDOW_WIDTH
        self.message_font = ResourceManager.load_font("Timetwist-Regular.ttf", 30)
        self.button_font = ResourceManager.load_font("Timetwist-Regular.ttf", 22)

    def _mouse_button_down(self, event):
        if self.replay_button_y.collidepoint(event.pos):
                from game import Game
                self.director.change_scene(Game(self.director))
        elif self.quit_button.collidepoint(event.pos):
                self.director.exit_program()

    def draw(self, display_surface):
        draw_background(display_surface, self.background)
        display_label(display_surface,"Enhorabuena! has hecho justicia",self.message_x, self.message_y, self.message_font)
        self._draw_buttons(display_surface)



    def _draw_buttons(self, display_surface):
        button_width = WINDOW_WIDTH * 0.2
        button_height = WINDOW_HEIGHT * 0.1
        self.replay_button_y = draw_button(
            display_surface,
            "REPLAY",
            self.button_font,
            0.45 * WINDOW_HEIGHT,
            width=button_width,
            height=button_height
        )

        self.quit_button = draw_button(
            display_surface,
            "QUIT",
            self.button_font,
            0.5833 * WINDOW_HEIGHT,
            width=button_width,
            height=button_height
        )
