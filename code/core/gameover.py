#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
import pygame
from pygame import Surface

from code.system.managers.assetmanager import AssetManager
from code.system.controllers.audiocontroller import AudioController
from code.system.config import WIN_WIDTH, WIN_HEIGHT
from code.factory.entityFactory import EntityFactory

class GameOver:
    def __init__(self, window: Surface):
        self.window = window
        self.bg_layers = EntityFactory.get_entity("GameOverBg")

        # Sprites
        self.mora_dead = AssetManager.get_image("MoraDead.png")
        self.leon_dead = AssetManager.get_image("LeonDead.png")
        self.text = AssetManager.get_image("GameOverText.png")

        # Resize e posicionamento

        self.clock = pygame.time.Clock()
        self.angle = 0

    def show(self):
        AudioController().play_music("gameover")

        while True:
            self.clock.tick(60)
            self.angle = 5 * math.sin(pygame.time.get_ticks() * 0.002)

            self._draw_background()
            self._draw_overlay()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        return

    def _draw_background(self):
        for ent in self.bg_layers:
            ent.move()
            self.window.blit(ent.surf, ent.rect)

    def _draw_overlay(self):
        ticks = pygame.time.get_ticks()
        t = ticks * 0.005

        offset_leon = math.sin(t * 0.9) * 1.5
        offset_mora = math.cos(t * 1.1) * 1.8
        angle_leon = 2.5 * math.sin(t * 0.7)
        angle_mora = 2.5 * math.cos(t * 0.6)

        leon_rotated = pygame.transform.rotate(self.leon_dead, angle_leon)
        rect_leon = leon_rotated.get_rect(center=(WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 + offset_leon))
        self.window.blit(leon_rotated, rect_leon)

        mora_rotated = pygame.transform.rotate(self.mora_dead, angle_mora)
        rect_mora = mora_rotated.get_rect(center=(WIN_WIDTH // 2 + 100, WIN_HEIGHT // 2 + offset_mora))
        self.window.blit(mora_rotated, rect_mora)

        scale = 1 + 0.01 * math.sin(t * 0.8)
        offset_text_y = math.sin(t * 0.4) * 2
        text_scaled = pygame.transform.rotozoom(self.text, 0, scale)
        rect_text = text_scaled.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + offset_text_y))
        self.window.blit(text_scaled, rect_text)

