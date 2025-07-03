import os
import pygame


class AssetManager:
    _image_cache = {}
    _font_cache = {}
    _sound_cache = {}

    IMAGE_DIR = "asset/images"
    SOUND_DIR = "asset/sounds"
    FONT_DIR = "asset/fonts"

    @staticmethod
    def get_image(filename: str) -> pygame.Surface:
        # Garante que tenha extensão
        if not filename.lower().endswith(".png"):
            filename += ".png"

        if filename in AssetManager._image_cache:
            return AssetManager._image_cache[filename]

        # 1. Tenta caminho direto
        path = os.path.join(AssetManager.IMAGE_DIR, filename)
        if os.path.isfile(path):
            try:
                image = pygame.image.load(path).convert_alpha()
                AssetManager._image_cache[filename] = image
                return image
            except Exception as e:
                print(f"[Erro ao carregar imagem direta '{filename}']: {e}")

        # 2. Busca recursiva ignorando maiúsculas/minúsculas
        filename_lower = filename.lower()
        for root, _, files in os.walk(AssetManager.IMAGE_DIR):
            for file in files:
                if file.lower() == filename_lower:
                    try:
                        full_path = os.path.join(root, file)
                        image = pygame.image.load(full_path).convert_alpha()
                        AssetManager._image_cache[filename] = image
                        return image
                    except Exception as e:
                        print(f"[Erro ao carregar imagem '{filename}' em subpasta]: {e}")

        print(f"[Imagem não encontrada: {filename}]")
        return pygame.Surface((1, 1), pygame.SRCALPHA)

    @staticmethod
    def get_sound(filename: str) -> pygame.mixer.Sound:
        if not filename.lower().endswith(".mp3") and not filename.lower().endswith(".wav"):
            filename += ".mp3"  # ou ajuste se quiser forçar .wav por padrão

        if filename in AssetManager._sound_cache:
            return AssetManager._sound_cache[filename]

        # Caminho direto
        path = os.path.join(AssetManager.SOUND_DIR, filename)
        if os.path.isfile(path):
            try:
                sound = pygame.mixer.Sound(path)
                AssetManager._sound_cache[filename] = sound
                return sound
            except Exception as e:
                print(f"[Erro ao carregar som direto '{filename}']: {e}")

        # Busca recursiva
        filename_lower = filename.lower()
        for root, _, files in os.walk(AssetManager.SOUND_DIR):
            for file in files:
                if file.lower() == filename_lower:
                    try:
                        full_path = os.path.join(root, file)
                        sound = pygame.mixer.Sound(full_path)
                        AssetManager._sound_cache[filename] = sound
                        return sound
                    except Exception as e:
                        print(f"[Erro ao carregar som '{filename}' em subpasta]: {e}")

        print(f"[Som não encontrado: {filename}]")
        return pygame.mixer.Sound(buffer=pygame.mixer.Sound(b"\x00").get_raw())

    @staticmethod
    def get_font(filename: str, size: int) -> pygame.font.Font:
        key = (filename, size)
        if key in AssetManager._font_cache:
            return AssetManager._font_cache[key]

        if not filename.lower().endswith(".ttf"):
            filename += ".ttf"

        path = os.path.join(AssetManager.FONT_DIR, filename)
        if os.path.isfile(path):
            try:
                font = pygame.font.Font(path, size)
                AssetManager._font_cache[key] = font
                return font
            except Exception as e:
                print(f"[Erro ao carregar fonte direta '{filename}']: {e}")

        filename_lower = filename.lower()
        for root, _, files in os.walk(AssetManager.FONT_DIR):
            for file in files:
                if file.lower() == filename_lower:
                    try:
                        full_path = os.path.join(root, file)
                        font = pygame.font.Font(full_path, size)
                        AssetManager._font_cache[key] = font
                        return font
                    except Exception as e:
                        print(f"[Erro ao carregar fonte '{filename}' em subpasta]: {e}")

        print(f"[Fonte não encontrada: {filename}]")
        return pygame.font.SysFont("Arial", size)

