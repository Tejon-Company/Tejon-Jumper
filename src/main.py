from settings import *
from director import Director
from scene.level import Level
from pytmx.util_pygame import load_pygame
from os.path import join


if __name__ == "__main__":
    pygame.init()
    director = Director()
    scene = Level(director)
    director.stack_scene(scene)
    director.run()
    pygame.quit()
