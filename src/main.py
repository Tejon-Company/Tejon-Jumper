from settings import *
from director import Director
from scene.level import Level


if __name__ == "__main__":
    pygame.init()
    director = Director()
    scene = Level(director)
    director.stack_scene(scene)
    director.run()
    pygame.quit()
