from dataclasses import dataclass

from singletons.singleton_meta import SingletonMeta


class ResolutionSettings(metaclass=SingletonMeta):
    """
    Gestiona la configuración de resolución para el juego.
    Permite alternar entre diferentes resoluciones predefinidas (HD, Full HD)
    y proporciona acceso a los parámetros relevantes de la resolución actual como
    nombre, ancho y alto de ventana, y tamaño de los sprites.
    """

    @dataclass(frozen=True)
    class _Resolution:
        _name: str
        _window_width: int
        _window_height: int
        _tile_size: int

    def __init__(self):
        self._resolutions = (
            ResolutionSettings._Resolution("hd", 1280, 720, 32),
            ResolutionSettings._Resolution("full_hd", 1880, 1030, 48),
        )
        self._current = 0

    @property
    def name(self) -> str:
        return self._resolutions[self._current]._name

    @property
    def window_width(self) -> int:
        return self._resolutions[self._current]._window_width

    @property
    def window_height(self) -> int:
        return self._resolutions[self._current]._window_height

    @property
    def tile_size(self) -> int:
        return self._resolutions[self._current]._tile_size

    def update_resolution(self):
        self._current = (self._current + 1) % len(self._resolutions)
        from singletons.director import Director

        director = Director()
        director.update_display_surface_resolution()
