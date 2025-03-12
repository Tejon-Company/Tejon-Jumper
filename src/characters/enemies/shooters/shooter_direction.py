from enum import Enum
from settings import *


class ShooterDirection(Enum):
    LEFT = (vector(-1, 0), 3)
    RIGHT = (vector(1, 0), 6)
    UP = (vector(0, -1), 0)
    DOWN = (vector(0, 1), 0)

    @classmethod
    def obtain_direction(cls, orientation):
        match(orientation.upper()):
            case "LEFT":
                return ShooterDirection.LEFT
            case "RIGHT":
                return ShooterDirection.RIGHT
            case "UP":
                return ShooterDirection.UP
            case "DOWN":
                return ShooterDirection.DOWN
            case _:
                raise ValueError(
                    f"The orientation {orientation} does not exist\n")
