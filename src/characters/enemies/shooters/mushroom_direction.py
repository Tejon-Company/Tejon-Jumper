from settings import *


class MushroomDirection(Enum):
    LEFT = (vector(-1, 0), 3)
    RIGHT = (vector(1, 0), 6)
    UP = (vector(0, -1), 0)
    DOWN = (vector(0, 1), 0)

    @classmethod
    def obtain_direction(cls, orientation):
        match(orientation.upper()):
            case "LEFT":
                return MushroomDirection.LEFT
            case "RIGHT":
                return MushroomDirection.RIGHT
            case "UP":
                return MushroomDirection.UP
            case "DOWN":
                return MushroomDirection.DOWN
            case _:
                raise ValueError(
                    f"The orientation {orientation} does not exist\n")
