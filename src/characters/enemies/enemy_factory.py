from settings import *
from characters.enemies.moving_enemies.hedgehog import Hedgehog
from characters.enemies.shooters.mushroom import Mushroom
from characters.enemies.moving_enemies.fox import Fox
from characters.enemies.moving_enemies.bat import Bat
from characters.enemies.moving_enemies.bear import Bear
from characters.enemies.shooters.squirrel import Squirrel
from characters.enemies.shooters.mushroom_direction import MushroomDirection


def enemy_factory(enemy, groups, platform_rects, spore_pool, acorn_pool, player, game):
    match enemy.name:
        case "Hedgehog":
            Hedgehog(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["moving_enemies"], groups["enemies"]),
                player,
                platform_rects,
                "hedgehog.png",
                _create_animation_rects(0, 2),
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
                _create_animation_rects(direction.value[1], 3),
                game,
                spore_pool
            )
        case "Fox":
            Fox(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["moving_enemies"], groups["enemies"]),
                player,
                platform_rects,
                "fox.png",
                _create_animation_rects(0, 3),
                game
            )
        case "Bear":
            Bear(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["moving_enemies"], groups["enemies"]),
                player,
                platform_rects,
                "bear.png",
                _create_animation_rects(0, 4, sprite_width=64),
                game
            )
        case "Bat":
            Bat(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["moving_enemies"], groups["enemies"]),
                player,
                "bat.png",
                _create_animation_rects(0, 3),
                game
            )
        case "Squirrel":
            Squirrel(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["all_sprites"], groups["enemies"]),
                player,
                "squirrel.png",
                _create_animation_rects(1, 2),
                game,
                acorn_pool
            )
        case _:
            raise ValueError(
                f"The entitie {enemy.name} is not a valid entitie")


def _create_animation_rects(frame_start_x, number_of_frames, sprite_width = TILE_SIZE):
    sprite_height = TILE_SIZE
    frame_start_x *= sprite_width
    y = 0
    pixel_gap = 1
    animation_rects = []

    for i in range(number_of_frames):
        x = (frame_start_x + frame_start_x//32) + \
            (sprite_width * i) + (i * pixel_gap)
        animation_rects.append((x, y, sprite_width, sprite_height))

    return animation_rects
