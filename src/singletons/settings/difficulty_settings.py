from singletons.singleton_meta import SingletonMeta
from dataclasses import dataclass


class DifficultySettings(metaclass=SingletonMeta):
    """
    Clase que gestiona las configuraciones de dificultad del juego.
    Permite definir y alternar entre diferentes niveles de dificultad,
    afectando parámetros como la salud y vidas del jugador, así como la salud del enemigo final.
    """

    @dataclass(frozen=True)
    class _Difficulty:
        name: str
        player_health_points: int
        player_lives: int
        bear_health_points: int

    def __init__(self):
        self._difficulties = (
            DifficultySettings._Difficulty("Fácil", 5, 3, 3),
            DifficultySettings._Difficulty("Difícil", 3, 1, 5),
        )
        self._current = 0

    @property
    def name(self) -> str:
        return self._difficulties[self._current].name

    @property
    def player_health_points(self) -> int:
        return self._difficulties[self._current].player_health_points

    @property
    def player_lives(self) -> int:
        return self._difficulties[self._current].player_lives

    @property
    def bear_health_points(self) -> int:
        return self._difficulties[self._current].bear_health_points

    def update_difficulty(self):
        self._current = (self._current + 1) % len(self._difficulties)
