from settings import *
from director import Director
from scene.level1 import Level1


if __name__ == "__main__":
    pygame.init()
    director = Director()
    scene = Level1(director)
    director.stack_scene(scene)
    director.run()
    pygame.quit()
