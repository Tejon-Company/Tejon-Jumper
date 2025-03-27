from singletons.singleton_meta import SingletonMeta
from dataclasses import dataclass


class ResolutionSettings(metaclass=SingletonMeta):
    @dataclass(frozen=True)
    class _Resolution:
        name: str
        window_width: int
        window_height: int
        tile_size: int

    def __init__(self):
        self._resolutions = (
            ResolutionSettings._Resolution("hd", 1280, 720, 32),
            ResolutionSettings._Resolution("full_hd", 1920, 1050, 48),
        )
        self._current = 0

    @property
    def name(self) -> str:
        return self._resolutions[self._current].name

    @property
    def window_width(self) -> int:
        return self._resolutions[self._current].window_width

    @property
    def window_height(self) -> int:
        return self._resolutions[self._current].window_height

    @property
    def tile_size(self) -> int:
        return self._resolutions[self._current].tile_size

    def update_resolution(self):
        self._current = (self._current + 1) % len(self._resolutions)
