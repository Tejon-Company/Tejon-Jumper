from berries.health_berry import HealthBerry
from berries.coin_berrie import CoinBerry
from berries.energy_berry import EneryBerry
from berries.rage_berry import RageBerry


def berrie_factory(berrie, groups):
    match berrie.name:
        case "health_berrie":
            HealthBerry(
                (berrie.x, berrie.y),
                berrie.image,
                (groups["berries"])
            )
        case "coin_berrie":
            CoinBerry(
                (berrie.x, berrie.y),
                berrie.image,
                (groups["berries"])
            )
        case "energy_berrie":
            EneryBerry(
                (berrie.x, berrie.y),
                berrie.image,
                (groups["berries"])
            )
        case "rage_berrie":
            RageBerry(
                (berrie.x, berrie.y),
                berrie.image,
                (groups["berries"])
            )
        case _:
            raise ValueError(
                f"The entitie {berrie.name} is not a valid berrie")
