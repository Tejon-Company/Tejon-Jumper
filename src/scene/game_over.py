import pygame
from settings import config
from scene.scene import Scene


class GameOver(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from game import Game
                self.director.change_scene(Game(self.director))

    def draw(self, display_surface):
        display_surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, (255, 0, 0))
        display_surface.blit(text, (config.window_width // 2 - text.get_width() //
                             2, config.window_height // 2 - text.get_height() // 2))
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Restart", True, (255, 255, 255))
        display_surface.blit(text, (config.window_width // 2 - text.get_width() //
                             2, config.window_height // 2 + text.get_height()))
