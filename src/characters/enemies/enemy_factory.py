from settings import *
from characters.players.player import Player
from characters.enemies.moving_enemies.hedgehog import Hedgehog
from characters.enemies.shooters.mushroom import Mushroom


def enemy_factory(enemy, groups):
    match enemy.name:
        case "Hedgehog":
            Hedgehog(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["hedgehogs"]),
            )
        case "Mushroom":
            Mushroom(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["mushrooms"]),
            )
        case default:
            raise ValueError(f"The entitie {enemy.name} is not a valid entitie")
