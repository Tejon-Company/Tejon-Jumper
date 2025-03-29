from singletons.settings.resolution_settings import ResolutionSettings
from sprites.characters.enemies.moving_enemies.bat import Bat
from sprites.characters.enemies.moving_enemies.fox import Fox
from sprites.characters.enemies.moving_enemies.hedgehog import Hedgehog
from sprites.characters.enemies.shooters.mushroom import Mushroom
from sprites.characters.enemies.shooters.mushroom_direction import MushroomDirection
from sprites.characters.enemies.shooters.squirrel import Squirrel
from sprites.characters.utils.animation_utils import create_animation_rects


def enemy_factory(enemy, groups, platform_rects, spore_pool, acorn_pool, player):
    """
    Crea un enemigo específico según su tipo, añadiéndolo a los grupos correspondientes.
    Args:
        enemy: Objeto enemigo a crear con su posición, imagen y nombre.
        groups: Diccionario con los diferentes grupos de sprites para añadir al enemigo.
        platform_rects: Lista de rectángulos de plataformas para la colisión.
        spore_pool: Pool de proyectiles de esporas para el enemigo Mushroom.
        acorn_pool: Pool de proyectiles de bellotas para el enemigo Squirrel.
        player: Referencia al jugador para seguimiento y comportamiento.
    Raises:
        KeyError: Si un enemigo Mushroom no tiene definida su orientación.
        ValueError: Si el tipo de enemigo no es válido.
    """

    resolution_settings = ResolutionSettings()
    match enemy.name:
        case "Hedgehog":
            Hedgehog(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["moving_enemies"], groups["characters"]),
                player,
                platform_rects,
                "hedgehog.png",
                create_animation_rects(0, 2, resolution_settings.tile_size),
            )
        case "Mushroom":
            orientation = enemy.properties.get("Orientation", None)
            if orientation is None:
                raise KeyError("The orientation property is not found")

            direction = MushroomDirection.obtain_direction(orientation)
            Mushroom(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["characters"], groups["platforms"], groups["shooters"]),
                direction.value[0],
                player,
                "mushroom.png",
                create_animation_rects(
                    direction.value[1], 3, resolution_settings.tile_size
                ),
                spore_pool,
            )
        case "Fox":
            Fox(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["characters"], groups["moving_enemies"]),
                player,
                platform_rects,
                "fox.png",
                create_animation_rects(0, 3, resolution_settings.tile_size),
            )
        case "Bat":
            Bat(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["moving_enemies"], groups["characters"]),
                player,
                "bat.png",
                create_animation_rects(0, 3, resolution_settings.tile_size),
            )
        case "Squirrel":
            Squirrel(
                (enemy.x, enemy.y),
                enemy.image,
                (groups["characters"], groups["shooters"]),
                player,
                "squirrel.png",
                create_animation_rects(1, 2, resolution_settings.tile_size),
                acorn_pool,
            )
        case _:
            raise ValueError(f"The enemy {enemy.name} is not a valid enemy")
