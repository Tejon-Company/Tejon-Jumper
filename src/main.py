import pygame

from scene.menus.main_menu import MainMenu
from singletons.director import Director

if __name__ == "__main__":
    pygame.init()
    director = Director()
    director.push_scene(MainMenu())
    director.run()
    pygame.quit()
