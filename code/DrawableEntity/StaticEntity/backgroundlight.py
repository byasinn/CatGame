import pygame

from code.system.assetmanager import AssetManager
from code.system.entity import Entity

class BackgroundLight(Entity):
    def __init__(self, name: str, position: tuple):
        self.original_name = name
        self.image = AssetManager.get_image(f"{name}.png")
        win = pygame.display.get_surface()
        w, h = win.get_size()
        self.surf = pygame.transform.scale(self.image, (w, h))
        self.rect = self.surf.get_rect(topleft=position)
        self.name = name
        self.health = 999
        self.damage = 0
        self.score = 0
        self.last_dmg = "None"

    def move(self):
        pass  # não se move
