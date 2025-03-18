from environment.rock import Rock


def environment_factory(enviroment_element, groups):
    match enviroment_element.name:
        case "Rock":
            Rock(
                (enviroment_element.x, enviroment_element.y),
                enviroment_element.image,
                (groups["environment"], groups["platforms"])
            )
        case _:
            raise ValueError(
                f"The entitie {enviroment_element.name} is not a valid enviroment element")