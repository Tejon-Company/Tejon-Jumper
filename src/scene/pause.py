import pygame
from scene.scene import Scene
from resource_manager import ResourceManager
from settings import *


class Pause(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

        self.music_volume = pygame.mixer.music.get_volume()
        self.effects_volume = ResourceManager.get_effects_volume()
        
    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self.director.exit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_btn.collidepoint(event.pos):
                    self.director.pop_scene()
                if self.restart_btn.collidepoint(event.pos):
                    from scene.level import Level
                    self.director.change_scene(Level(self.director))
                if self.music_volume_bar.collidepoint(event.pos):
                    self.music_volume = (event.pos[0] - self.music_volume_bar.x) / self.music_volume_bar.width
                    ResourceManager.set_music_volume(self.music_volume)
                if self.effects_volume_bar.collidepoint(event.pos):
                    self.effects_volume = (event.pos[0] - self.effects_volume_bar.x) / self.effects_volume_bar.width
                    ResourceManager.set_effects_volume(self.effects_volume)
                    
    def draw(self, display_surface):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))  
        display_surface.blit(overlay, (0, 0)) 
        
        font = pygame.font.Font(None, 40)

        self.pause_menu = pygame.Rect(
            WINDOW_WIDTH // 2 - 125, WINDOW_HEIGHT // 2 - 300, 200, 50)
        self.continue_btn = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100, 200, 50)
        self.restart_btn = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50)
        self.music_volume_bar = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 20)
        self.effects_volume_bar = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 150, 200, 20)

        self._draw_menu_text(display_surface, self.pause_menu, "Pause Menu", font)
        
        self._draw_button(display_surface, self.continue_btn, "Continue", font)
        self._draw_button(display_surface, self.restart_btn, "Restart", font)

        self._draw_volume_bar(display_surface, self.music_volume_bar, self.music_volume, "Music", font)
        self._draw_volume_bar(display_surface, self.effects_volume_bar, self.effects_volume, "Sound Effects", font)


    def _draw_menu_text(self, display_surface, rect, text, font):
        pause_menu_text = font.render(text, True, (0, 0, 0))
        text_rect = pause_menu_text.get_rect(center=(rect.centerx, rect.centery))
        display_surface.blit(pause_menu_text, text_rect.topleft)
        
    def _draw_button(self, display_surface, rect, text, font):
        pygame.draw.rect(display_surface, (0, 0, 255), rect)
        text_surf = font.render(text, True, (255, 255, 255))
        display_surface.blit(text_surf, (rect.x + 40, rect.y + 15))

    def _draw_volume_bar(self, display_surface, rect, volume, label, font):
        pygame.draw.rect(display_surface, (255, 255, 255), rect)
        pygame.draw.rect(display_surface, (0, 255, 0), (rect.x, rect.y, volume * rect.width, rect.height))
        label_surf = font.render(label, True, (0, 0, 0))
        display_surface.blit(label_surf, (rect.x - label_surf.get_width() - 10, rect.y))