#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.const import  ENTITY_SPEED, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.entity import Entity
from code.playershot import PlayerShot


class Player(Entity):
    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.damage_flash_timer = 0

    def move(self, ):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < self.window.get_width():
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < self.window.get_width():
            self.rect.centerx += ENTITY_SPEED[self.name]



        pass

    def shoot(self):
        pressed_key = pygame.key.get_pressed()
        if self.shot_delay > 0:
            self.shot_delay -= 1
        if pressed_key[PLAYER_KEY_SHOOT[self.name]] and self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]

            # Som do tiro (carrega e toca o som correspondente ao jogador)
            try:
                sound = pygame.mixer.Sound(f"./asset/{self.name}Shot.mp3")
                sound.set_volume(0.5)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som de tiro] {e}")

            return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        return None

    def take_damage_flash(self):
        self.damage_flash_timer = 10  # quantos frames ele vai piscar vermelho
