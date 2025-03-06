from settings import *
from os.path import join
from pygame.transform import scale
from pygame.image import load


class HUD:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        lives_font_path = join('assets', 'fonts', 'Beta54.ttf')
        self.font = pygame.font.Font(lives_font_path, 22)

        player_icon_path = join('assets', 'badger_icon.png')
        self.player_icon = scale(load(player_icon_path), (32, 32))

        self._setup_coin_icon()

    def _setup_coin_icon(self):
        coin_icon_path = join(
            'assets', 'creatures_and_else', 'berries', 'without_background', 'berries.png')

        coin_icon_image = load(coin_icon_path).convert_alpha()

        icon = coin_icon_image.subsurface((98, 0, 32, 32))
        icon = scale(icon, (32, 32))

        self.coin_icon = icon

    def draw_hud(self, remaining_health_points: int, remaining_lives: int, coins: int):
        self._draw_hearts(remaining_health_points)
        self._draw_lifes_counter(remaining_lives)
        self._draw_coins_counter(coins)

    def _draw_hearts(self, remaining_health_points):
        heart_size = 32
        heart_color = (255, 0, 0)
        spacing = 10
        start_x = 10
        start_y = 10

        for i in range(remaining_health_points):
            pygame.draw.rect(
                self.display_surface,
                heart_color,
                (start_x + i * (heart_size + spacing),
                 start_y, heart_size, heart_size)
            )

    def _draw_lifes_counter(self, remaining_lives: int):
        self.display_surface.blit(self.player_icon, (10, 50))
        lives_text = f"x{remaining_lives}"
        text_surface = self.font.render(lives_text, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (50, 50))

    def _draw_coins_counter(self, coins: int):
        coin_icon = self.coin_icon

        margin = 10
        coin_icon_x = self.display_surface.get_width() - coin_icon.get_width() - 40
        coin_icon_y = margin

        self.display_surface.blit(coin_icon, (coin_icon_x, coin_icon_y))

        coins_text = f"x{coins}"
        text_surface = self.font.render(coins_text, True, (255, 255, 255))

        text_x = coin_icon_x + coin_icon.get_width() + 5
        text_y = coin_icon_y

        self.display_surface.blit(text_surface, (text_x, text_y))
