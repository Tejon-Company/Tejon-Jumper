from scene.scene import Scene
from singletons.settings.resolution_settings import ResolutionSettings
import pygame


class GameOver(Scene):
    def __init__(self):
        super().__init__()
        self.resolution_settings = ResolutionSettings()
        self.display_surface = pygame.display.get_surface()

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from scene.level import Level

                first_level = Level(1)
                self.director.change_scene(first_level)

    def draw(self, display_surface):
        display_surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, (255, 0, 0))
        display_surface.blit(
            text,
            (
                self.resolution_settings.window_width // 2 - text.get_width() // 2,
                self.resolution_settings.window_height // 2 - text.get_height() // 2,
            ),
        )
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Restart", True, (255, 255, 255))
        display_surface.blit(
            text,
            (
                self.resolution_settings.window_width // 2 - text.get_width() // 2,
                self.resolution_settings.window_height // 2 + text.get_height(),
            ),
        )
