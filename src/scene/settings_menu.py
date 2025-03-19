from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from scene.scene import Scene
from resource_manager import ResourceManager
from settings import *
import pygame


class SettingsMenu(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

        X = WINDOW_WIDTH // 2
        Y = WINDOW_HEIGHT // 2
        WIDTH = 200
        HEIGHT = 50
        VOLUME_BAR_HEIGHT = 20

        self.music_volume_bar = Rect(
            X - WIDTH // 2, Y - 150, WIDTH, VOLUME_BAR_HEIGHT)
        self.effects_volume_bar = Rect(
            X - WIDTH // 2, Y - 100, WIDTH, VOLUME_BAR_HEIGHT)

        self.difficulty_btn = Rect(X - WIDTH // 2, Y - 30, WIDTH, HEIGHT)
        self.resolution_btn = Rect(X - WIDTH // 2, Y + 50, WIDTH, HEIGHT)
        self.back_btn = Rect(X - WIDTH // 2, Y + 130, WIDTH, HEIGHT)

        self.music_volume = pygame.mixer.music.get_volume()
        self.effects_volume = ResourceManager.get_effects_volume()

        self.difficulty_levels = ["Easy", "Hard"]
        self.current_difficulty = 1

        self.resolutions = [(800, 600), (1280, 720), (1920, 1080)]
        self.current_resolution = 1

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event)

    def _mouse_button_down(self, event):
        if self.music_volume_bar.collidepoint(event.pos):
            self.music_volume = (
                event.pos[0] - self.music_volume_bar.x) / self.music_volume_bar.width
            ResourceManager.set_music_volume(self.music_volume)

        elif self.effects_volume_bar.collidepoint(event.pos):
            self.effects_volume = (
                event.pos[0] - self.effects_volume_bar.x) / self.effects_volume_bar.width
            ResourceManager.set_effects_volume(self.effects_volume)

        elif self.difficulty_btn.collidepoint(event.pos):
            self.current_difficulty = (
                self.current_difficulty + 1) % len(self.difficulty_levels)

        # elif self.resolution_btn.collidepoint(event.pos):
        #    self.current_resolution = (self.current_resolution + 1) % len(self.resolutions)
        #    pygame.display.set_mode(self.resolutions[self.current_resolution])

        elif self.back_btn.collidepoint(event.pos):
            from scene.menu import Menu
            self.director.change_scene(Menu(self.director))

    def draw(self, display_surface):
        display_surface.fill((50, 50, 50))
        font = ResourceManager.load_font('Timetwist-Regular.ttf', 20)

        self._draw_volume_bar(
            display_surface, self.music_volume_bar, self.music_volume, "Music", font)
        self._draw_volume_bar(display_surface, self.effects_volume_bar,
                              self.effects_volume, "Sound Effects", font)

        game_mode_label = font.render("Game Mode", True, 'white')
        display_surface.blit(
            game_mode_label, (self.difficulty_btn.x - 150, self.difficulty_btn.y + 15))

        self._draw_button(display_surface, self.difficulty_btn,
                          f"{self.difficulty_levels[self.current_difficulty]}", font)

        resolution_label = font.render("Resolution", True, 'white')
        display_surface.blit(
            resolution_label, (self.resolution_btn.x - 135, self.resolution_btn.y + 15))

        self._draw_button(display_surface, self.resolution_btn,
                          f"{self.resolutions[self.current_resolution][0]}x{self.resolutions[self.current_resolution][1]}", font)

        self._draw_button(display_surface, self.back_btn, "Return", font)

    def _draw_button(self, display_surface, rect, text, font):
        draw_rect(display_surface, 'black', rect)
        text_surf = font.render(text, True, 'white')
        text_rect = text_surf.get_rect(center=rect.center)
        display_surface.blit(text_surf, text_rect.topleft)

    def _draw_volume_bar(self, display_surface, rect, volume, label, font):
        draw_rect(display_surface, 'white', rect)
        draw_rect(display_surface, 'green',
                  (rect.x, rect.y, volume * rect.width, rect.height))
        label_surf = font.render(label, True, 'white')
        display_surface.blit(
            label_surf, (rect.x - label_surf.get_width() - 10, rect.y))
