import pygame
from code.system.managers.assetmanager import AssetManager
from code.system.entity import Entity

class BackgroundLight(Entity):
    def __init__(self, name: str, position: tuple):
        self.original_name = name
        self.name = name
        self.image = AssetManager.get_image(f"{name}.png")
        win = pygame.display.get_surface()
        if not win:
            raise RuntimeError("Surface não disponível ao instanciar BackgroundLight.")

        w, h = win.get_size()
        extra_w = int(w * 0.1)
        extra_h = int(h * 0.1)
        scaled_w = w + extra_w
        scaled_h = h + extra_h

        self.surf = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (-extra_w // 2, -extra_h // 2)
        self.health = 999
        self.damage = 0
        self.score = 0
        self.last_dmg = "None"

    def move(self):
        pass
