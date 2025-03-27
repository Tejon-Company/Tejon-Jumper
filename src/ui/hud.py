from resource_manager import ResourceManager
from singletons.settings.resolution_settings import ResolutionSettings
import pygame


class HUD:
    display_surface = None
    sprite_size = None
    font = None
    font_size = None
    player_icon = None
    health_icon = None
    coin_icon = None
    energy_icon = None
    bear_health_icon = None

    @classmethod
    def initialize(cls, sprite_size, font_size):
        cls.resolution_settings = ResolutionSettings()
        cls.sprite_size = sprite_size
        cls.font_size = font_size
        cls.font = ResourceManager.load_font("Beta54.ttf", cls.font_size)

        cls.player_icon = ResourceManager.load_image("badger_icon.png")

        cls._setup_health_icon()
        cls._setup_coin_icon()
        cls._setup_energy_icon()
        cls._setup_bear_health_icon()

    @classmethod
    def _setup_health_icon(cls):
        health_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        health_icon = health_icon_image.subsurface(
            (0, 0, cls.sprite_size, cls.sprite_size)
        )

        cls.health_icon = health_icon

    @classmethod
    def _setup_coin_icon(cls):
        coin_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        coin_icon = coin_icon_image.subsurface(
            (((cls.sprite_size * 3) + 2), 0, cls.sprite_size, cls.sprite_size)
        )

        cls.coin_icon = coin_icon

    @classmethod
    def _setup_energy_icon(cls):
        energy_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        energy_icon = energy_icon_image.subsurface(
            (((cls.sprite_size * 2) + 1), 0, cls.sprite_size, cls.sprite_size)
        )

        cls.energy_icon = energy_icon

    @classmethod
    def _setup_bear_health_icon(cls):
        bear_health_icon_image = ResourceManager.load_sprite_sheet("bear_heart.png")

        bear_health_icon = bear_health_icon_image.subsurface(
            (0, 0, cls.sprite_size, cls.sprite_size)
        )

        cls.bear_health_icon = bear_health_icon

    @classmethod
    def draw_hud(
        cls,
        display_surface,
        remaining_health_points: int,
        remaining_lives: int,
        coins: int,
        energy: int,
        bear_health_points: int,
    ):
        cls._draw_hearts(display_surface, remaining_health_points)
        cls._draw_energy_bar(display_surface, energy)
        cls._draw_lifes_counter(display_surface, remaining_lives)
        cls._draw_coins_counter(display_surface, coins)
        cls._draw_bear_hearts(display_surface, bear_health_points)

    @classmethod
    def _draw_icon_with_counter(cls, display_surface, icon, count: int, x: int, y: int):
        display_surface.blit(icon, (x, y))
        count_text = f"x{count}"
        text_surface = cls.font.render(count_text, True, (255, 255, 255))
        display_surface.blit(text_surface, (x + icon.get_width() + 5, y))

    @classmethod
    def _draw_health_icons(
        cls, display_surface, health_points: int, icon, start_x: int, start_y: int
    ):
        heart_size = 32
        spacing = 10
        for i in range(health_points):
            display_surface.blit(icon, (start_x + i * (heart_size + spacing), start_y))

    @classmethod
    def _draw_hearts(cls, display_surface, remaining_health_points):
        cls._draw_health_icons(
            display_surface, remaining_health_points, cls.health_icon, 10, 10
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

        pygame.draw.rect(
            display_surface, border_color, (bar_x, start_y, bar_width, bar_height), 2
        )

        energy_width = int((energy / 100) * (bar_width - 4))
        pygame.draw.rect(
            display_surface,
            fill_color,
            (bar_x + 2, start_y + 2, energy_width, bar_height - 4),
        )

        icon_x = start_x
        icon_y = start_y + (bar_height - 32) // 2
        display_surface.blit(cls.energy_icon, (icon_x, icon_y))

    @classmethod
    def _draw_lifes_counter(cls, display_surface, remaining_lives: int):
        cls._draw_icon_with_counter(
            display_surface, cls.player_icon, remaining_lives, 10, 90
        )

    @classmethod
    def _draw_coins_counter(cls, display_surface, coins: int):
        coin_icon_x = display_surface.get_width() - cls.coin_icon.get_width() - 40
        cls._draw_icon_with_counter(
            display_surface, cls.coin_icon, coins, coin_icon_x, 10
        )

    @classmethod
    def _draw_bear_hearts(cls, display_surface, bear_healt_points: int):
        start_x = (
            cls.resolution_settings.window_width // 2
            - cls.resolution_settings.tile_size * 2
        )
        cls._draw_health_icons(
            display_surface, bear_healt_points, cls.bear_health_icon, start_x, 10
        )
