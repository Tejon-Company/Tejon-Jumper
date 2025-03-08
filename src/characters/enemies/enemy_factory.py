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
                "hedgehog.png",
                _create_animation_rects(0, 2)
            )
        case "Mushroom":
            Mushroom(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"],
                 groups["mushrooms"], groups["platforms"]),
                player,
                "mushroom.png",
                _create_animation_rects(0, 1),
                spore_pool
            )
        case "Fox":
            Fox(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["foxes"]),
                "fox.png",
                _create_animation_rects(0, 3),
            )
        case "Bat":
            Bat(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["bats"]),
                "bat.png",
                _create_animation_rects(0, 0),
            )
        case "Squirrel":
            Squirrel(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["squirrels"]),
                player,
                "squirrel.png",
                _create_animation_rects(32, 2),
                acorn_pool
            )
        case _:
            raise ValueError(
                f"The entitie {enemy.name} is not a valid entitie")


def _create_animation_rects(start_x, number_of_frames):
    sprite_size = TILE_SIZE
    y = 0
    pixel_gap = 1
    animation_rects = []

    for i in range(number_of_frames):
        x = (start_x + start_x//32) + (sprite_size * i) + (i * pixel_gap)
        animation_rects.append((x, y, sprite_size, sprite_size))

    return animation_rects
