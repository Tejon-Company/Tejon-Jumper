from settings import *
from os.path import join
from pygame.transform import scale
from pygame.image import load
from resource_manager import ResourceManager


class HUD:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        lives_font_path = join('Beta54.ttf')
        self.font = ResourceManager.load_font(lives_font_path, 22)

        player_icon_path = join('assets', 'badger_icon.png')
        self.player_icon = scale(load(player_icon_path), (32, 32))

        self._setup_health_icon()

    def draw_hud(self, remaining_health_points: int, remaining_lives: int):
        self._draw_hearts(remaining_health_points)
        self._draw_lifes_counter(remaining_lives)
        self._draw_energy_bar(100)

    def _draw_hearts(self, remaining_health_points):
        heart_size = 32
        spacing = 10
        start_x = 10
        start_y = 10

        for i in range(remaining_health_points):
            self.display_surface.blit(
                self.health_icon,
                (start_x + i * (heart_size + spacing), start_y)
            )

    def _draw_lifes_counter(self, remaining_lives: int):
        self.display_surface.blit(self.player_icon, (10, 50))
        lives_text = f"x{remaining_lives}"
        text_surface = self.font.render(lives_text, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (50, 50))

    def _setup_health_icon(self):
        health_icon_path = join(
            'assets', 'creatures_and_else', 'berries', 'without_background', 'berries.png')
        health_icon_image = load(health_icon_path)
        health_icon_image = health_icon_image.convert_alpha()

        first_icon = health_icon_image.subsurface((0, 0, 32, 32))
        first_icon = scale(first_icon, (32, 32))

        self.health_icon = first_icon

    def _draw_energy_bar(self, energy: float):
            bar_width = 150
            bar_height = 15
            start_x = 10
            start_y = 90  
            border_color = (255, 255, 255)
            fill_color = (255, 255, 0) 

            pygame.draw.rect(self.display_surface, border_color, (start_x, start_y, bar_width, bar_height), 2)

            energy_width = int((energy / 100) * (bar_width - 4))  
            pygame.draw.rect(self.display_surface, fill_color, (start_x + 2, start_y + 2, energy_width, bar_height - 4))
