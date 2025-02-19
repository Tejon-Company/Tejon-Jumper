from settings import *
from character import Character


class Enemy(Character):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

    