#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pygame.image
from code.system.config import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE
from pygame.transform import scale

class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        loaded = pygame.image.load('./asset/' + name + '.png').convert_alpha()
        scale_factor = self.get_scale_factor()  # calcula baseado na janela
        new_size = (int(loaded.get_width() * scale_factor), int(loaded.get_height() * scale_factor))
        self.surf = scale(loaded, new_size)
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
