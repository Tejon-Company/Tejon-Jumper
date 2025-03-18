from characters.sprite import Sprite


class EnvironmentElement(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)