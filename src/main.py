from settings import *
from director import Director
from game import Game


if __name__ == "__main__":
    pygame.init()
    director = Director()
    game = Game(director)
    director.stack_scene(game)
    director.run()
    pygame.quit()
