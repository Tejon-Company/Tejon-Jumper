from settings import *
from characters.enemies.moving_enemies.hedgehog import Hedgehog
from characters.enemies.shooters.mushroom import Mushroom
from characters.enemies.moving_enemies.fox import Fox
from characters.enemies.moving_enemies.bat import Bat
from characters.enemies.shooters.squirrel import Squirrel


def enemy_factory(enemy, groups, spore_pool, acorn_pool, player):
    match enemy.name:
        case "Hedgehog":
            Hedgehog(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["hedgehogs"]),
                "hedgehog.png"
            )
        case "Mushroom":
            Mushroom(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"],
                 groups["mushrooms"], groups["platforms"]),
                player,
                "mushroom.png",
                spore_pool
            )
        case "Fox":
            Fox(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["foxes"]),
                "fox.png"
            )
        case "Bat":
            Bat(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["bats"]),
                "bat.png"
            )
        case "Squirrel":
            Squirrel(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"],
                 groups["squirrels"]),
                player,
                "squirrel.png",
                acorn_pool
            )
        case _:
            raise ValueError(
                f"The entitie {enemy.name} is not a valid entitie")
