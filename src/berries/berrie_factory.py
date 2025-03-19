from berries.health_berry import HealthBerry
from berries.coin_berry import CoinBerry
from berries.energy_berry import EnergyBerry


def berry_factory(berry, groups):
    match berry.name:
        case "health_berry":
            HealthBerry(
                (berry.x, berry.y),
                berry.image,
                (groups["berries"])
            )
        case "coin_berry":
            CoinBerry(
                (berry.x, berry.y),
                berry.image,
                (groups["berries"])
            )
        case "energy_berry":
            EnergyBerry(
                (berry.x, berry.y),
                berry.image,
                (groups["berries"])
            )
        case _:
            raise ValueError(
                f"The entitie {berry.name} is not a valid berry")
