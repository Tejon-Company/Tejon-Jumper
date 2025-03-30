from sprites.sprite import Sprite
from abc import ABC


class EnvironmentElement(Sprite, ABC):
    """
    Base para diferentes elementos que componen el entorno del juego,
    permitiendo una interacción común con el jugador.
    """

    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
