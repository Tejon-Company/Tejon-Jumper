import pygame
from scene.scene import Scene
from resource_manager import ResourceManager
from settings import *


class Pause(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.display_surface = pygame.display.get_surface()

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

        self.music_volume = pygame.mixer.music.get_volume()
        self.effects_volume = pygame.mixer.Sound.get_volume(pygame.mixer.Sound) 
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
                elif self.music_volume_bar.collidepoint(event.pos):
                    print("Music volume pressed")
                    self.music_volume = (event.pos[0] - self.music_volume_bar.x) / self.music_volume_bar.width
                    ResourceManager.set_music_volume(self.music_volume)
                elif self.effects_volume_bar.collidepoint(event.pos):
                    print("Effects volume pressed")
                    self.effects_volume = (event.pos[0] - self.effects_volume_bar.x) / self.effects_volume_bar.width
                    ResourceManager.set_effects_volume(self.effects_volume)

    def draw(self, display_surface):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))  
        display_surface.blit(overlay, (0, 0)) 
        
        font = pygame.font.Font(None, 40)

        pygame.draw.rect(display_surface, (255, 0, 0), self.continue_btn)
        pygame.draw.rect(display_surface, (255, 0, 0), self.restart_btn)

        pause_menu_text = font.render("Pause Menu", True, (0, 0, 0))

        continue_text = font.render("Continue", True, (255, 255, 255))
        restart_text = font.render("Restart", True, (255, 255, 255))

        display_surface.blit(
            pause_menu_text, (self.pause_menu.x + 30, self.pause_menu.y + 15))

        display_surface.blit(
            continue_text, (self.continue_btn.x + 40, self.continue_btn.y + 15))
        display_surface.blit(
            restart_text, (self.restart_btn.x + 50, self.restart_btn.y + 15))

        pygame.draw.rect(display_surface, (255, 255, 255),
                         self.music_volume_bar)
        pygame.draw.rect(display_surface, (255, 255, 255),
                         self.effects_volume_bar)

        pygame.draw.rect(display_surface, (0, 255, 0), (self.music_volume_bar.x, self.music_volume_bar.y,
                         self.music_volume * self.music_volume_bar.width, self.music_volume_bar.height))
        pygame.draw.rect(display_surface, (0, 255, 0), (self.effects_volume_bar.x, self.effects_volume_bar.y,
                         self.effects_volume * self.effects_volume_bar.width, self.effects_volume_bar.height))
