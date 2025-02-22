from enum import Enum, auto


class PlayerState(Enum):
    ALIVE = auto()
    DAMAGED = auto()
    DEAD = auto()
    GAME_OVER = auto()
