import pygame

from resource_manager import ResourceManager
from singletons.settings.resolution_settings import ResolutionSettings


class HUD:
    """
    Gestiona la interfaz gráfica de usuario que muestra información relevante durante el juego,
    como la salud del jugador, vidas restantes, monedas recolectadas, energía y salud del oso.
    Dibuja varios elementos en la pantalla:
    - Corazones que representan la salud del jugador
    - Barra de energía
    - Contador de vidas
    - Contador de monedas
    - Corazones que representan la salud del oso
    """

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
    def initialize(cls):
        cls.resolution_settings = ResolutionSettings()
        cls.font_size = int(cls.resolution_settings.tile_size * 0.7)
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
            (0, 0, cls.resolution_settings.tile_size, cls.resolution_settings.tile_size)
        )

        cls.health_icon = health_icon

    @classmethod
    def _setup_coin_icon(cls):
        coin_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        coin_icon = coin_icon_image.subsurface(
            (
                ((cls.resolution_settings.tile_size * 3) + 2),
                0,
                cls.resolution_settings.tile_size,
                cls.resolution_settings.tile_size,
            )
        )

        cls.coin_icon = coin_icon

    @classmethod
    def _setup_energy_icon(cls):
        energy_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        energy_icon = energy_icon_image.subsurface(
            (
                ((cls.resolution_settings.tile_size * 2) + 1),
                0,
                cls.resolution_settings.tile_size,
                cls.resolution_settings.tile_size,
            )
        )

        cls.energy_icon = energy_icon

    @classmethod
    def _setup_bear_health_icon(cls):
        bear_health_icon_image = ResourceManager.load_sprite_sheet("bear_heart.png")

        bear_health_icon = bear_health_icon_image.subsurface(
            (0, 0, cls.resolution_settings.tile_size, cls.resolution_settings.tile_size)
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
        cls._draw_player_lifes_counter(display_surface, remaining_lives)
        cls._draw_coins_counter(display_surface, coins)
        cls._draw_bear_hearts(display_surface, bear_health_points)

    @classmethod
    def _draw_icon_with_counter(cls, display_surface, icon, count: int, x: int, y: int):
        display_surface.blit(icon, (x, y))
        count_text = f"x{count}"
        text_surface = cls.font.render(count_text, True, "white")
        display_surface.blit(text_surface, (x + cls.resolution_settings.tile_size, y))

    @classmethod
    def _draw_health_icons(
        cls, display_surface, health_points: int, icon, start_x: int, start_y: int
    ):
        heart_size = cls.resolution_settings.tile_size
        spacing = cls.resolution_settings.tile_size // 5
        for i in range(health_points):
            display_surface.blit(icon, (start_x + i * (heart_size + spacing), start_y))

    @classmethod
    def _draw_hearts(cls, display_surface, remaining_health_points):
        cls._draw_health_icons(
            display_surface, remaining_health_points, cls.health_icon, 10, 10
        )

    @classmethod
    def _draw_energy_bar(cls, display_surface, energy: float):
        bar_width = cls.resolution_settings.window_width * 0.15
        bar_height = cls.resolution_settings.tile_size // 2
        icon_width = cls.resolution_settings.tile_size
        icon_spacing = cls.resolution_settings.tile_size // 4
        start_x = cls.resolution_settings.tile_size // 5
        start_y = cls.resolution_settings.tile_size * 1.6

        bar_x = start_x - cls.resolution_settings.tile_size + icon_width + icon_spacing

        pygame.draw.rect(
            display_surface, "white", (bar_x, start_y, bar_width, bar_height), 2
        )

        energy_width = int((energy / 100) * (bar_width - 4))
        pygame.draw.rect(
            display_surface,
            "yellow",
            (bar_x + 2, start_y + 2, energy_width, bar_height - 4),
        )

        icon_x = start_x
        icon_y = start_y + (bar_height - cls.resolution_settings.tile_size) // 2
        display_surface.blit(cls.energy_icon, (icon_x, icon_y))

    @classmethod
    def _draw_player_lifes_counter(cls, display_surface, remaining_lives: int):
        cls._draw_icon_with_counter(
            display_surface,
            cls.player_icon,
            remaining_lives,
            cls.resolution_settings.tile_size // 5,
            cls.resolution_settings.tile_size * 2.5,
        )

    @classmethod
    def _draw_coins_counter(cls, display_surface, coins: int):
        coin_icon_x = (
            display_surface.get_width()
            - cls.coin_icon.get_width()
            - cls.resolution_settings.tile_size
        )
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
