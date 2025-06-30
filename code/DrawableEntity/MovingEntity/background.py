#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.system.config import ENTITY_SPEED
from code.system.entity import Entity


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.original_surf = self.surf.copy()
        self.rescale_to_window()

    def rescale_to_window(self):
        win = pygame.display.get_surface()
        if win:
            w, h = win.get_size()
            self.surf = pygame.transform.scale(self.original_surf, (w, h))

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.rect.right <= 0:
            self.rect.left = pygame.display.get_surface().get_width()
