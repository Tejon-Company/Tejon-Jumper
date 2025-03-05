import pygame
import os

class ResourceManager:
    resources = {}

    @classmethod
    def LoadImage(cls, name, colorkey=None):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = os.path.join('assets', 'images', name)  
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
    def LoadSound(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = os.path.join('assets', name)
            try:
                sound = pygame.mixer.Sound(fullname)
                cls.resources[name] = sound
                return sound
            except pygame.error as e:
                print(f"Error loading sound {fullname}: {e}")
                return None

    @classmethod
    def LoadMusic(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = os.path.join('assets', name)
            try:
                music = pygame.mixer.music.load(fullname)
                cls.resources[name] = music
                return music
            except pygame.error as e:
                print(f"Error loading music {fullname}: {e}")
                return None

    @classmethod
    def LoadFont(cls, name, size):
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
    def LoadAnimation(cls, name, num_frames, width, height):
        if name in cls.resources:
            return cls.resources[name]
        else:
            animation = []
            for i in range(num_frames):
                image = pygame.image.load(os.path.join('assets', 'animations', f'{name}_{i}.png')).convert_alpha()
                image = pygame.transform.scale(image, (width, height))
                animation.append(image)
            cls.resources[name] = animation
            return animation

    @classmethod
    def LoadSprite(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = os.path.join('assets', 'sprites', name)
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
