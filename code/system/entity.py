#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pygame.image

from code.system.assetmanager import AssetManager
from code.system.config import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE
from pygame.transform import scale

class Entity(ABC):
    def __init__(self, name: str, position: tuple, scale_image=True):
        self.name = name
        loaded = AssetManager.get_image(name + ".png")

        if scale_image:
            scale_factor = self.get_scale_factor()
            new_size = (int(loaded.get_width() * scale_factor), int(loaded.get_height() * scale_factor))
            self.surf = scale(loaded, new_size)
        else:
            self.surf = loaded

        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = "None"

    def get_scale_factor(self):
        # Ajuste conforme o tamanho base esperado.
        base_width = 576
        from pygame.display import get_surface
        surface = get_surface()
        if not surface:
            return 1.0
        current_width = surface.get_width()
        return current_width / base_width

    @abstractmethod
    def move(self, ):
        pass
