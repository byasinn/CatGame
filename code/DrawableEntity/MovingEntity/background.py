#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random

import pygame
from code.system.config import ENTITY_SPEED
from code.system.entity import Entity


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        self.bg_name = name
        base_name = name.lower().split(".")[0]
        self.apply_custom_rescale = not base_name.startswith("level") and not base_name.startswith("light")

        super().__init__(name, position)

        self.original_surf = self.surf.copy()

        if self.apply_custom_rescale:
            self.rescale_to_window()

    def rescale_to_window(self):
        win = pygame.display.get_surface()
        if win:
            w, h = win.get_size()

            extra_w = int(w * 0.1)
            extra_h = int(h * 0.1)
            self.surf = pygame.transform.scale(
                self.original_surf,
                (w + extra_w, h + extra_h)
            )
            self.rect = self.surf.get_rect()
            self.rect.topleft = (-extra_w // 2, -extra_h // 2)

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