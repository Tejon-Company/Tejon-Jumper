from settings import *
from singletons.director import Director
from scene.menus.main_menu import MainMenu


if __name__ == "__main__":
    pygame.init()
    director = Director()
    director.stack_scene(MainMenu(director))
    director.run()
    pygame.quit()
