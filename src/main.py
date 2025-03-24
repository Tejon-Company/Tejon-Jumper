from settings import *
from singletons.director import Director
from scene.menus.main_menu import MainMenu


if __name__ == "__main__":
    pygame.init()
    director = Director()
    director.push_scene(MainMenu())
    director.run()
    pygame.quit()
