from settings import *


class UI:
    def __init__(self, display_surface, player):
        self.display_surface = display_surface
        self.player = player
        # Option 1: Use a different system font size
        self.font = pygame.font.Font(None, 48)  # Larger size

        # Option 2: Load a custom font file
        self.font = pygame.font.Font('path/to/your/font.ttf', 36)

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
        lives_text = f"Remaining Lives: {remaining_lives}"
        text_surface = self.font.render(lives_text, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (10, 50))
