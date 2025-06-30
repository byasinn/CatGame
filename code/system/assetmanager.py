import os
import pygame

class AssetManager:
    _image_cache = {}
    _font_cache = {}
    _sound_cache = {}

    @staticmethod
    def get_image(filename: str) -> pygame.Surface:
        if filename in AssetManager._image_cache:
            return AssetManager._image_cache[filename]

        path = os.path.join("asset", filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            AssetManager._image_cache[filename] = image
            return image
        except Exception as e:
            print(f"[Erro ao carregar imagem '{filename}']: {e}")
            return pygame.Surface((1, 1), pygame.SRCALPHA)

    @staticmethod
    def get_sound(filename: str) -> pygame.mixer.Sound:
        if filename in AssetManager._sound_cache:
            return AssetManager._sound_cache[filename]

        path = os.path.join("asset", filename)
        try:
            sound = pygame.mixer.Sound(path)
            AssetManager._sound_cache[filename] = sound
            return sound
        except Exception as e:
            print(f"[Erro ao carregar som '{filename}']: {e}")
            return pygame.mixer.Sound(buffer=pygame.mixer.Sound(b"\x00").get_raw())

    @staticmethod
    def get_font(filename: str, size: int) -> pygame.font.Font:
        key = (filename, size)
        if key in AssetManager._font_cache:
            return AssetManager._font_cache[key]

        path = os.path.join("asset", filename)
        try:
            font = pygame.font.Font(path, size)
            AssetManager._font_cache[key] = font
            return font
        except Exception as e:
            print(f"[Erro ao carregar fonte '{filename}']: {e}")
            return pygame.font.SysFont("Arial", size)
