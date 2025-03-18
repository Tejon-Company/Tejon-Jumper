from characters.sprite import Sprite


class EnvironmentElement(Sprite):
    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups)