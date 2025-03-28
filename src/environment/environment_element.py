from characters.sprite import Sprite


class EnvironmentElement(Sprite):
    """
    Base para diferentes elementos que componen el entorno del juego,
    permitiendo una interacción común con el jugador.
    """

    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
