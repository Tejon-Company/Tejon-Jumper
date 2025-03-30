import pygame

from resource_manager import ResourceManager
from singletons.settings.resolution_settings import ResolutionSettings


class HUD:
    """
    Gestiona la interfaz gráfica de usuario que muestra información
    relevante durante el juego, como la salud del jugador, vidas
    restantes, monedas recolectadas, energía y salud del oso. Dibuja
    los siguientes elementos en la pantalla:

    - Corazones que representan la salud del jugador

    - Barra de energía

    - Contador de vidas

    - Contador de monedas

    - Corazones que representan la salud del oso
    """

    def __init__(self):
        self.resolution_settings = ResolutionSettings()
        self.font_size = int(self.resolution_settings.tile_size * 0.7)
        self.font = ResourceManager.load_font("Beta54.ttf", self.font_size)

        self.player_icon = ResourceManager.load_image("badger_icon.png")

        self._setup_health_icon()
        self._setup_coin_icon()
        self._setup_energy_icon()
        self._setup_bear_health_icon()

    def _setup_health_icon(self):

        health_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        health_icon = health_icon_image.subsurface(
            (
                0,
                0,
                self.resolution_settings.tile_size,
                self.resolution_settings.tile_size,
            )
        )

        self.health_icon = health_icon

    def _setup_coin_icon(self):

        coin_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        coin_icon = coin_icon_image.subsurface(
            (
                ((self.resolution_settings.tile_size * 3) + 3),
                0,
                self.resolution_settings.tile_size,
                self.resolution_settings.tile_size,
            )
        )

        self.coin_icon = coin_icon

    def _setup_energy_icon(self):

        energy_icon_image = ResourceManager.load_sprite_sheet("berries.png")

        energy_icon = energy_icon_image.subsurface(
            (
                ((self.resolution_settings.tile_size * 2) + 2),
                0,
                self.resolution_settings.tile_size,
                self.resolution_settings.tile_size,
            )
        )

        self.energy_icon = energy_icon

    def _setup_bear_health_icon(self):

        bear_health_icon_image = ResourceManager.load_sprite_sheet("bear_heart.png")

        bear_health_icon = bear_health_icon_image.subsurface(
            (
                0,
                0,
                self.resolution_settings.tile_size,
                self.resolution_settings.tile_size,
            )
        )

        self.bear_health_icon = bear_health_icon

    def draw_hud(
        self,
        display_surface,
        remaining_health_points: int,
        remaining_lives: int,
        coins: int,
        energy: int,
        bear_health_points: int,
    ):
        self._draw_hearts(display_surface, remaining_health_points)
        self._draw_energy_bar(display_surface, energy)
        self._draw_player_lifes_counter(display_surface, remaining_lives)
        self._draw_coins_counter(display_surface, coins)
        self._draw_bear_hearts(display_surface, bear_health_points)

    def _draw_icon_with_counter(
        self, display_surface, icon, count: int, x: int, y: int
    ):
        display_surface.blit(icon, (x, y))
        count_text = f"x{count}"
        text_surface = self.font.render(count_text, True, "white")
        display_surface.blit(text_surface, (x + self.resolution_settings.tile_size, y))

    def _draw_health_icons(
        self, display_surface, health_points: int, icon, start_x: int, start_y: int
    ):
        heart_size = self.resolution_settings.tile_size
        spacing = self.resolution_settings.tile_size // 5
        for i in range(health_points):
            display_surface.blit(icon, (start_x + i * (heart_size + spacing), start_y))

    def _draw_hearts(self, display_surface, remaining_health_points):
        self._draw_health_icons(
            display_surface, remaining_health_points, self.health_icon, 10, 10
        )

    def _draw_energy_bar(self, display_surface, energy: float):
        bar_width = self.resolution_settings.window_width * 0.15
        bar_height = self.resolution_settings.tile_size // 2
        icon_width = self.resolution_settings.tile_size
        icon_spacing = self.resolution_settings.tile_size // 4
        start_x = self.resolution_settings.tile_size // 5
        start_y = self.resolution_settings.tile_size * 1.6

        bar_x = start_x - self.resolution_settings.tile_size + icon_width + icon_spacing

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
        icon_y = start_y + (bar_height - self.resolution_settings.tile_size) // 2
        display_surface.blit(self.energy_icon, (icon_x, icon_y))

    def _draw_player_lifes_counter(self, display_surface, remaining_lives: int):
        self._draw_icon_with_counter(
            display_surface,
            self.player_icon,
            remaining_lives,
            self.resolution_settings.tile_size // 5,
            self.resolution_settings.tile_size * 2.5,
        )

    def _draw_coins_counter(self, display_surface, coins: int):
        coin_icon_x = (
            display_surface.get_width()
            - self.coin_icon.get_width()
            - int(self.resolution_settings.tile_size * 1.5)
        )
        self._draw_icon_with_counter(
            display_surface, self.coin_icon, coins, coin_icon_x, 10
        )

    def _draw_bear_hearts(self, display_surface, bear_healt_points: int):
        start_x = (
            self.resolution_settings.window_width // 2
            - self.resolution_settings.tile_size * 2
        )
        self._draw_health_icons(
            display_surface, bear_healt_points, self.bear_health_icon, start_x, 10
        )
