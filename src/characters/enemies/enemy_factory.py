from settings import *
from characters.players.player import Player
from characters.enemies.moving_enemies.hedgehog import Hedgehog
from characters.enemies.shooters.mushroom import Mushroom
from characters.enemies.moving_enemies.fox import Fox
from characters.enemies.shooters.squirrel import Squirrel


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
                (groups["all_sprites"],
                 groups["mushrooms"], groups["platforms"]),
                (groups["all_sprites"], groups["projectiles"])
            )
        case "Fox":
            Fox(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["foxes"]),
            )
        case "Squirrel":
            Squirrel(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"],
                 groups["squirrels"]),
                (groups["all_sprites"], groups["projectiles"])
            )
        case _:
            raise ValueError(
                f"The entitie {enemy.name} is not a valid entitie")
