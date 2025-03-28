from environment.flag import Flag
from environment.rock import Rock


def environment_factory(enviroment_element, groups, player, level):
    """
    Crea instancias de diferentes elementos del entorno basándose en el nombre del elemento.

    Args:
        enviroment_element: Objeto que contiene la información del elemento a crear (nombre, posición, imagen).
        groups: Grupos de sprites a los que se añadirá el elemento creado.
        player: Referencia al jugador para interacción con los elementos.
        level: Nivel actual del juego, necesario para elementos como la bandera.

    Raises:
        ValueError: Si se proporciona un nombre de elemento no soportado.
    """
    match enviroment_element.name:
        case "Rock":
            Rock(
                (enviroment_element.x, enviroment_element.y),
                enviroment_element.image,
                groups,
                player,
            )
        case "Flag":
            Flag(
                (enviroment_element.x, enviroment_element.y),
                enviroment_element.image,
                groups,
                player,
                level,
            )
        case _:
            raise ValueError(
                f"The entitie {enviroment_element.name} is not a valid enviroment element"
            )
