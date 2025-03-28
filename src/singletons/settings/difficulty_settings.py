from dataclasses import dataclass

from singletons.singleton_meta import SingletonMeta


class DifficultySettings(metaclass=SingletonMeta):
    """
    Gestiona las configuraciones de dificultad del juego.
    Permite definir y alternar entre diferentes niveles de dificultad,
    afectando parámetros como la salud y vidas del jugador, así como la salud del enemigo final.
    """

    @dataclass(frozen=True)
    class _Difficulty:
        _name: str
        _player_health_points: int
        _player_lives: int
        _bear_health_points: int

    def __init__(self):
        self._difficulties = (
            DifficultySettings._Difficulty("Fácil", 5, 3, 3),
            DifficultySettings._Difficulty("Difícil", 3, 1, 5),
        )
        self._current = 0

    @property
    def name(self) -> str:
        return self._difficulties[self._current]._name

    @property
    def player_health_points(self) -> int:
        return self._difficulties[self._current]._player_health_points

    @property
    def player_lives(self) -> int:
        return self._difficulties[self._current]._player_lives

    @property
    def bear_health_points(self) -> int:
        return self._difficulties[self._current]._bear_health_points

    def update_difficulty(self):
        self._current = (self._current + 1) % len(self._difficulties)
