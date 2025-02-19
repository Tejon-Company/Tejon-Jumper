from settings import *
from entities.players.player import Player
from entities.enemies.hedgehog import Hedgehog


def entitie_factory(entitie, groups):
    match entitie.name:
        case "Player":
            Player((entitie.x, entitie.y), entitie.image, groups["all_sprites"])
        case "Hedgehog":
            Hedgehog(
                (entitie.x, entitie.y),
                entitie.image,
                (groups["all_sprites"], groups["hedgehogs"]),
            )
        case default:
            raise ValueError(f"The entitie {entitie.name} is not a valid entitie")
