import pygame


class Sprite(pygame.sprite.Sprite):
    """
    Implementa un sprite básico en el juego con una imagen y posición.
    """

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
