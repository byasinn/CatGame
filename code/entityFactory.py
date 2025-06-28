#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import pygame

from code.background import Background
from code.backgroundlight import BackgroundLight
from code.boss import Boss
from code.enemy import Enemy
from code.player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        surface = pygame.display.get_surface()
        match entity_name:
            case "Level1Bg":
                width = surface.get_width()
                list_bg = []
                for i in range(6):
                    bg_left = Background(f'Level1Bg{i}', (0, 0))
                    bg_right = Background(f'Level1Bg{i}', (width, 0))
                    list_bg.extend([bg_left, bg_right])
                list_bg.append(BackgroundLight("LightOverlay_Level1", (0, 0)))
                return list_bg
            case "Level2Bg":
                width = surface.get_width()
                list_bg = []
                for i in range(4):
                    bg_left = Background(f'Level2Bg{i}', (0, 0))
                    bg_right = Background(f'Level2Bg{i}', (width, 0))
                    list_bg.extend([bg_left, bg_right])
                list_bg.append(BackgroundLight("LightOverlay_Level2", (0, 0)))
                return list_bg
            case "Level3Bg":
                width = surface.get_width()
                list_bg = []
                for i in range(6):
                    bg_left = Background(f'Level3Bg{i}', (0, 0))
                    bg_right = Background(f'Level3Bg{i}', (width, 0))
                    list_bg.extend([bg_left, bg_right])
                list_bg.append(BackgroundLight("LightOverlay_Level2", (0, 0)))
                return list_bg
            case "Player1":
                return Player("Player1", (10, surface.get_height() / 2 - 30), surface)
            case "Player2":
                return Player("Player2", (10, surface.get_height() / 2 + 30), surface)
            case "Enemy1":
                return Enemy("Enemy1", (surface.get_width() + 10, random.randint(30, surface.get_height() - 30)), surface)
            case "Enemy2":
                return Enemy("Enemy2", (surface.get_width() + 10, random.randint(30, surface.get_height() - 30)), surface)

            case "Boss":
                return Enemy("Boss", (surface.get_width() + 10, random.randint(30, surface.get_height() - 30)), surface)

            case "GameOverBg":
                list_bg = []
                for i in range(3):
                    list_bg.append(Background(f'GameOverBg{i}', (0, 0)))
                    list_bg.append(Background(f'GameOverBg{i}', (pygame.display.get_surface().get_width(), 0)))
                list_bg.append(BackgroundLight("GameOverLight", (0, 0)))
                return list_bg
