from settings import *

class UI:
    def __init__(self, display_surface, player):
        self.display_surface = display_surface
        self.player = player

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
                (start_x + i * (heart_size + spacing), start_y, heart_size, heart_size) 
            ) 
