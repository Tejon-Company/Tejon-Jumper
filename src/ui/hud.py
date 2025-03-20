from settings import *
from os.path import join
from pygame.transform import scale
from pygame.image import load
from resource_manager import ResourceManager


class HUD:
    display_surface = None
    font = None
    player_icon = None
    health_icon = None
    coin_icon = None
    energy_icon = None
    bear_health_icon = None

    @classmethod
    def initialize(cls):
        lives_font_path = join('Beta54.ttf')
        cls.font = ResourceManager.load_font(lives_font_path, 22)

        player_icon_path = join('assets', 'badger_icon.png')
        cls.player_icon = scale(load(player_icon_path), (32, 32))

        cls._setup_health_icon()
        cls._setup_coin_icon()
        cls._setup_energy_icon()
        cls._setup_bear_health_icon()

    @classmethod
    def _setup_health_icon(cls):
        health_icon_path = join(
            'assets', 'creatures_and_else', 'berries', 'without_background', 'berries.png')
        health_icon_image = load(health_icon_path)
        health_icon_image = health_icon_image.convert_alpha()

        first_icon = health_icon_image.subsurface((0, 0, 32, 32))
        first_icon = scale(first_icon, (32, 32))

        cls.health_icon = first_icon

    @classmethod
    def _setup_coin_icon(cls):
        coin_icon_path = join(
            'assets', 'creatures_and_else', 'berries', 'without_background', 'berries.png')

        coin_icon_image = load(coin_icon_path).convert_alpha()

        icon = coin_icon_image.subsurface((98, 0, 32, 32))
        icon = scale(icon, (32, 32))

        cls.coin_icon = icon

    @classmethod
    def _setup_energy_icon(cls):
        energy_icon_path = 'berries.png'
        energy_icon_image = ResourceManager.load_sprite_sheet(energy_icon_path)

        first_icon = energy_icon_image.subsurface((65, 0, 32, 32))
        first_icon = scale(first_icon, (32, 32))

        cls.energy_icon = first_icon

    @classmethod
    def _setup_bear_health_icon(cls):
        health_icon_path = join(
            'assets', 'creatures_and_else', 'berries', 'without_background', 'berries.png')
        health_icon_image = load(health_icon_path)
        health_icon_image = health_icon_image.convert_alpha()

        first_icon = health_icon_image.subsurface((0, 0, 32, 32))
        first_icon = scale(first_icon, (32, 32))

        cls.bear_health_icon = first_icon

    @classmethod
    def draw_hud(cls, display_surface, remaining_health_points: int, remaining_lives: int, coins: int, energy: int, bear_health_points: int = 0):
        cls._draw_hearts(display_surface, remaining_health_points)
        cls._draw_energy_bar(display_surface, energy)
        cls._draw_lifes_counter(display_surface, remaining_lives)
        cls._draw_coins_counter(display_surface, coins)
        cls._draw_bear_hearts(display_surface, bear_health_points)

    @classmethod
    def _draw_hearts(cls, display_surface, remaining_health_points):
        heart_size = 32
        spacing = 10
        start_x = 10
        start_y = 10

        for i in range(remaining_health_points):
            display_surface.blit(
                cls.health_icon,
                (start_x + i * (heart_size + spacing), start_y)
            )

    @classmethod
    def _draw_energy_bar(cls, display_surface, energy: float):
        bar_width = 150
        bar_height = 15
        icon_width = 32
        icon_spacing = 10
        start_x = 5
        start_y = 60

        bar_x = start_x - 30 + icon_width + icon_spacing
        border_color = (255, 255, 255)
        fill_color = (255, 255, 0)

        pygame.draw.rect(display_surface, border_color,
                         (bar_x, start_y, bar_width, bar_height), 2)

        energy_width = int((energy / 100) * (bar_width - 4))
        pygame.draw.rect(display_surface, fill_color,
                         (bar_x + 2, start_y + 2, energy_width, bar_height - 4))

        icon_x = start_x
        icon_y = start_y + (bar_height - 32) // 2
        display_surface.blit(cls.energy_icon, (icon_x, icon_y))

    @classmethod
    def _draw_lifes_counter(cls, display_surface, remaining_lives: int):
        display_surface.blit(cls.player_icon, (10, 90))
        lives_text = f"x{remaining_lives}"
        text_surface = cls.font.render(lives_text, True, (255, 255, 255))
        display_surface.blit(text_surface, (50, 90))

    @classmethod
    def _draw_coins_counter(cls, display_surface, coins: int):
        coin_icon = cls.coin_icon

        margin = 10
        coin_icon_x = display_surface.get_width() - coin_icon.get_width() - 40
        coin_icon_y = margin

        display_surface.blit(coin_icon, (coin_icon_x, coin_icon_y))

        coins_text = f"x{coins}"
        text_surface = cls.font.render(coins_text, True, (255, 255, 255))

        text_x = coin_icon_x + coin_icon.get_width() + 5
        text_y = coin_icon_y

        display_surface.blit(text_surface, (text_x, text_y))

    @classmethod
    def _draw_bear_hearts(cls, display_surface, bear_healt_points: int):
        heart_size = 32
        spacing = 10
        start_x = WINDOW_WIDTH // 2 - TILE_SIZE * 2
        start_y = 10

        for i in range(bear_healt_points):
            display_surface.blit(
                cls.bear_health_icon,
                (start_x + i * (heart_size + spacing), start_y)
            )
