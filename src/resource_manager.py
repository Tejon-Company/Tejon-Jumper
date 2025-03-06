import pygame
import os
from os.path import join


class ResourceManager:
    resources = {}

    @classmethod
    def load_image(cls, name, colorkey=None):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = join('assets', name)
            try:
                image = pygame.image.load(fullname).convert_alpha()
                if colorkey:
                    image.set_colorkey(colorkey)
                cls.resources[name] = image
                return image
            except pygame.error as e:
                print(f"Error loading image {fullname}: {e}")
                return None

    @classmethod
    def load_sound(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = join('assets', 'sounds', 'sound_effects', name)
            try:
                sound = pygame.mixer.Sound(fullname)
                cls.resources[name] = sound
                return sound
            except pygame.error as e:
                print(f"Error loading sound {fullname}: {e}")
                return None

    @classmethod
    def load_music(cls, name):
        music_path = os.path.join('assets', 'sounds', 'music', name)
        try:
            pygame.mixer.music.load(music_path)
            cls.resources[name] = music_path
            return music_path
        except pygame.error as e:
            print(f"Error loading music {music_path}: {e}")
            return None

    @classmethod
    def load_font(cls, name, size):
        if (name, size) in cls.resources:
            return cls.resources[(name, size)]
        else:
            fullname = os.path.join('assets', 'fonts', name)
            try:
                font = pygame.font.Font(fullname, size)
                cls.resources[(name, size)] = font
                return font
            except pygame.error as e:
                print(f"Error loading font {fullname}: {e}")
                return None

    @classmethod
    def load_sprite(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = os.path.join('assets', 'creatures_and_else', name)
            try:
                image = pygame.image.load(fullname).convert_alpha()
                cls.resources[name] = image
                return image
            except pygame.error as e:
                print(f"Error loading sprite {fullname}: {e}")
                return None

    @classmethod
    def ClearResources(cls):
        cls.resources.clear()
