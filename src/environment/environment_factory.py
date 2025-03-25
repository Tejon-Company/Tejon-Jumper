from environment.rock import Rock
from environment.flag import Flag


def environment_factory(enviroment_element, groups, player, level):
    match enviroment_element.name:
        case "Rock":
            Rock(
                (enviroment_element.x, enviroment_element.y),
                enviroment_element.image,
                groups,
                player
            )
        case "Flag":
            Flag(
                (enviroment_element.x, enviroment_element.y),
                enviroment_element.image,
                groups,
                player,
                level
            )
        case _:
            raise ValueError(
                f"The entitie {enviroment_element.name} is not a valid enviroment element")
