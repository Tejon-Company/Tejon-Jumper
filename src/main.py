from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tejón Jumper")
        self.clock = pygame.time.Clock()

        self.tmx_maps = {
            0: {
                "map": load_pygame(join("assets", "maps", "levels", "level0.tmx")),
                "background": "background1",
                "music": "level_1.ogg"
            },
        }

        self.current_stage = Level(
            self.tmx_maps[0]["map"], self.tmx_maps[0]["background"], self.tmx_maps[0]["music"]
        )

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(delta_time)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
