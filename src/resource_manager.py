from os.path import join

import pygame
from pytmx.util_pygame import load_pygame

from singletons.settings.resolution_settings import ResolutionSettings


class ResourceManager:
    """
    Gestiona los recursos del juego como imágenes, sonidos, música,
    fuentes y mapas.
    """

    _resources = {}
    _effects_volume = 1.0
    _loaded_sounds = []
    _resolution_settings = ResolutionSettings()

    @classmethod
    def load_image(cls, name, colorkey=None):
        if name in cls._resources:
            return cls._resources[name]

        try:
            fullname = join("assets", cls._resolution_settings.name, name)
            image = pygame.image.load(fullname).convert_alpha()
            if colorkey:
                image.set_colorkey(colorkey)
            cls._resources[name] = image
            return image
        except Exception as e:
            print(f"Error loading image {name}: {e}")

    @classmethod
    def load_sound_effect(cls, name):
        if name in cls._resources:
            return cls._resources[name]

        try:
            fullname = join("assets", "sounds", "sound_effects", name)
            sound = pygame.mixer.Sound(fullname)
            sound.set_volume(cls._effects_volume)
            cls._resources[name] = sound
            cls._loaded_sounds.append(sound)
            return sound
        except Exception as e:
            print(f"Error loading sound {name}: {e}")

    @classmethod
    def load_music(cls, name):
        try:
            music_path = join("assets", "sounds", "music", name)
            pygame.mixer.music.load(music_path)
            cls._resources[name] = music_path
            return music_path
        except Exception as e:
            print(f"Error loading music {name}: {e}")

    @classmethod
    def load_font(cls, name, size):
        key = (name, size)
        if key in cls._resources:
            return cls._resources[key]

        try:
            fullname = join("assets", "fonts", name)
            font = pygame.font.Font(fullname, size)
            cls._resources[key] = font
            return font
        except Exception as e:
            print(f"Error loading font {name}: {e}")

    @classmethod
    def load_sprite_sheet(cls, name):
        if name in cls._resources:
            return cls._resources[name]

        try:
            fullname = join(
                "assets",
                cls._resolution_settings.name,
                "sprite_sheets",
                "day",
                name,
            )
            image = pygame.image.load(fullname).convert_alpha()
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
            cls._resources[name] = image
            return image
        except Exception as e:
            print(f"Error loading sprite {name}: {e}")

    @classmethod
    def load_tmx_map(cls, name):
        if name in cls._resources:
            return cls._resources[name]

        try:
            level_path = join(
                "assets",
                cls._resolution_settings.name,
                "tiled",
                "levels",
                name,
            )
            tmx_map = load_pygame(level_path)
            return tmx_map

        except Exception as e:
            print(f"Error loading map {name}: {e}")

    @classmethod
    def set_music_volume(cls, volume):
        pygame.mixer.music.set_volume(volume)

    @classmethod
    def get_music_volume(cls):
        return pygame.mixer.music.get_volume()

    @classmethod
    def set_effects_volume(cls, volume):
        cls._effects_volume = volume
        for sound in cls._loaded_sounds:
            sound.set_volume(volume)

    @classmethod
    def get_effects_volume(cls):
        return cls._effects_volume

    @classmethod
    def clear_resources(cls):
        cls._resources.clear()
