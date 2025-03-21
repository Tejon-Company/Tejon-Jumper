from settings import *
from director import Director
from scene.menu import Menu


if __name__ == "__main__":
    pygame.init()
    director = Director()
    director.stack_scene(Menu(director))
    director.run()
    pygame.quit()