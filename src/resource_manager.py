import pygame
from os.path import join
from pytmx.util_pygame import load_pygame


class ResourceManager:
    resources = {}
    effects_volume = 1.0
    loaded_sounds = []

    @classmethod
    def load_image(cls, name, colorkey=None):
        if name in cls.resources:
            return cls.resources[name]

        try:
            fullname = join("assets", name)
            image = pygame.image.load(fullname).convert_alpha()
            if colorkey:
                image.set_colorkey(colorkey)
            cls.resources[name] = image
            return image
        except Exception as e:
            print(f"Error loading image {fullname}: {e}")

    @classmethod
    def load_sound_effect(cls, name):
        if name in cls.resources:
            return cls.resources[name]

        try:
            fullname = join("assets", "sounds", "sound_effects", name)
            sound = pygame.mixer.Sound(fullname)
            sound.set_volume(cls.effects_volume)
            cls.resources[name] = sound
            cls.loaded_sounds.append(sound)
            return sound
        except Exception as e:
            print(f"Error loading sound {fullname}: {e}")

    @classmethod
    def load_music(cls, name):
        try:
            music_path = join("assets", "sounds", "music", name)
            pygame.mixer.music.load(music_path)
            cls.resources[name] = music_path
            return music_path
        except Exception as e:
            print(f"Error loading music {music_path}: {e}")

    @classmethod
    def load_font(cls, name, size):
        key = (name, size)
        if key in cls.resources:
            return cls.resources[key]

        try:
            fullname = join("assets", "fonts", name)
            font = pygame.font.Font(fullname, size)
            cls.resources[key] = font
            return font
        except Exception as e:
            print(f"Error loading font {fullname}: {e}")

    @classmethod
    def load_sprite_sheet(cls, name):
        if name in cls.resources:
            return cls.resources[name]

        try:
            fullname = join("assets", "hd", "sprite_sheets", "day", name)
            image = pygame.image.load(fullname).convert_alpha()
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
            cls.resources[name] = image
            return image
        except Exception as e:
            print(f"Error loading sprite {fullname}: {e}")

    @classmethod
    def load_tmx_map(cls, name):
        if name in cls.resources:
            return cls.resources[name]

        try:
            level_path = join("assets", "hd", "tiled", "levels", name)
            tmx_map = load_pygame(level_path)
            return tmx_map

        except Exception as e:
            print(f"Error loading map {level_path}: {e}")

    @classmethod
    def set_music_volume(cls, volume):
        pygame.mixer.music.set_volume(volume)

    @classmethod
    def get_music_volume(cls):
        return pygame.mixer.music.get_volume()

    @classmethod
    def set_effects_volume(cls, volume):
        cls.effects_volume = volume
        for sound in cls.loaded_sounds:
            sound.set_volume(volume)

    @classmethod
    def get_effects_volume(cls):
        return cls.effects_volume

    @classmethod
    def clear_resources(cls):
        cls.resources.clear()
