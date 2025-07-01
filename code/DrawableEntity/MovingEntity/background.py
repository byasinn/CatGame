#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random

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


class BackgroundFloat(Background):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.base_x, self.base_y = self.rect.topleft
        self.offset = random.randint(5, 20)
        self.speed = random.uniform(0.0005, 0.002)
        self.direction = random.choice([-1, 1])
        self.phase = random.uniform(0, math.pi * 2)

    def move(self):
        t = pygame.time.get_ticks()
        offset = math.sin(t * self.speed + self.phase) * self.offset
        self.rect.x = self.base_x + int(offset * self.direction)