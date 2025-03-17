from settings import *
from characters.enemies.moving_enemies.hedgehog import Hedgehog
from characters.enemies.shooters.mushroom import Mushroom
from characters.enemies.moving_enemies.fox import Fox
from characters.enemies.moving_enemies.bat import Bat
from characters.enemies.shooters.squirrel import Squirrel
from characters.enemies.shooters.mushroom_direction import MushroomDirection
from characters.animation_utils import create_animation_rects


def enemy_factory(enemy, groups, platform_rects, spore_pool, acorn_pool, player, game):
    match enemy.name:
        case "Hedgehog":
            Hedgehog(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["enemies"]),
                player,
                platform_rects,
                "hedgehog.png",
                create_animation_rects(0, 2, TILE_SIZE),
                game
            )
        case "Mushroom":
            orientation = enemy.properties.get("Orientation", None)
            if orientation is None:
                raise KeyError(
                    "The orientation property is not found")

            direction = MushroomDirection.obtain_direction(orientation)
            Mushroom(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["enemies"], groups["platforms"]),
                direction.value[0],
                player,
                "mushroom.png",
                create_animation_rects(direction.value[1], 3, TILE_SIZE),
                game,
                spore_pool
            )
        case "Fox":
            Fox(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["enemies"]),
                player,
                platform_rects,
                "fox.png",
                create_animation_rects(0, 3, TILE_SIZE),
                game
            )
        case "Bat":
            Bat(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["enemies"]),
                player,
                "bat.png",
                create_animation_rects(0, 0, TILE_SIZE),
                game
            )
        case "Squirrel":
            Squirrel(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["enemies"]),
                player,
                "squirrel.png",
                create_animation_rects(1, 2, TILE_SIZE),
                game,
                acorn_pool
            )
        case _:
            raise ValueError(
                f"The entitie {enemy.name} is not a valid entitie")
