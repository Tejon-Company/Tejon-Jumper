from settings import *
from os.path import join
from pygame.transform import scale
from pygame.image import load


class UI:
    def __init__(self, display_surface, player):
        self.display_surface = display_surface

        self.player = player

        lives_font_path = join('assets', 'fonts', 'Beta54.ttf')
        self.font = pygame.font.Font(lives_font_path, 22)

        player_icon_path = join('assets', 'badger_icon.png')
        self.player_icon = scale(load(player_icon_path), (32, 32))

    def draw_hearts(self):
        heart_size = 32
        heart_color = (255, 0, 0)
        spacing = 10
        start_x = 10
        start_y = 10

        for i in range(self.player.health_points):
            pygame.draw.rect(
                self.display_surface,
                heart_color,
                (start_x + i * (heart_size + spacing),
                 start_y, heart_size, heart_size)
            )

    def draw_lifes_counter(self, remaining_lives: int):
        self.display_surface.blit(self.player_icon, (10, 50))
        lives_text = f"x{remaining_lives}"
        text_surface = self.font.render(lives_text, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (50, 50))
