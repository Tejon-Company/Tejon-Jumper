from berries.health_berry import HealthBerry


def berrie_factory(berrie, groups):
    match berrie.name:
        case "Health Berry":
            HealthBerry(
                (berrie.x, berrie.y),
                berrie.image,
                (groups["berries"])
            )
        case _:
            raise ValueError(
                f"The entitie {berrie.name} is not a valid berrie")
