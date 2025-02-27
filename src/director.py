from settings import *


class Director():
    def __init__(self):
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tejón Jumper")

        self.stack = []
        self.exit_scene = False
        self.clock = pygame.time.Clock()

    def _loop(self, scene):
        self.exit_scene = False
        pygame.event.clear()

        while not self.exit_scene:
            delta_time = self.clock.tick(60) / 1000
            scene.events(pygame.event.get())
            scene.update(delta_time)
            scene.draw(self.display_surface)

            pygame.display.update()
            pygame.display.flip()

    def run(self):
        while (len(self.stack) > 0):
            scene = self.stack[-1]
            self._loop(scene)

    def pop_scene(self):
        self.exit_scene = True
        if (len(self.stack) > 0):
            self.stack.pop()

    def exit_program(self):
        self.stack = []
        self.exit_scene = True

    def change_scene(self, scene):
        self.pop_scene()
        self.stack.append(scene)

    def stack_scene(self, scene):
        self.exit_scene = True
        self.stack.append(scene)
