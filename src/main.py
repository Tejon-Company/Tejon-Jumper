from singletons.director import Director
from scene.ui.menus.main_menu import MainMenu
import pygame


if __name__ == "__main__":
    pygame.init()
    director = Director()
    director.push_scene(MainMenu())
    director.run()
    pygame.quit()
