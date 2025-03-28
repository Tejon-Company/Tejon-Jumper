from berries.health_berry import HealthBerry
from berries.coin_berry import CoinBerry
from berries.energy_berry import EnergyBerry
from berries.rage_berry import RageBerry


def berry_factory(berry, groups):
    """
    Factory que crea diferentes tipos de bayas según el nombre proporcionado.
    Args:
        berry: Objeto berry que contiene la información necesaria para crear la baya (nombre, posición, imagen).
        groups: Grupos de sprites a los que se añadirá la baya creada.
    Returns:
        None, pero crea y añade la baya correspondiente a los grupos especificados.
    Raises:
        ValueError: Si el nombre de la baya no corresponde a ninguno de los tipos válidos.
    """

    match berry.name:
        case "health_berry":
            HealthBerry((berry.x, berry.y), berry.image, groups)
        case "coin_berry":
            CoinBerry((berry.x, berry.y), berry.image, groups)
        case "energy_berry":
            EnergyBerry((berry.x, berry.y), berry.image, groups)
        case "rage_berry":
            RageBerry((berry.x, berry.y), berry.image, groups)
        case _:
            raise ValueError(f"The entity {berry.name} is not a valid berry")
