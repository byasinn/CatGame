#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

import pygame

from code.system.assetmanager import AssetManager
from code.system.config import ENTITY_SPEED, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.shots.playershot import PlayerShot
from code.CombatEntity.combatentity import CombatEntity
from code.system.particle import AuraBurstParticle

class Player(CombatEntity):
    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.damage_flash_timer = 0
        self.damage_counter = 0
        self.damage_timer = 0
        self.shot_fired = False

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < self.window.get_height():
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < self.window.get_width():
            self.rect.centerx += ENTITY_SPEED[self.name]

    def shoot(self):
        pressed_key = pygame.key.get_pressed()

        # Diminui o delay de tiro
        if self.shot_delay > 0:
            self.shot_delay -= 1

        # Verifica se pode atirar
        if pressed_key[PLAYER_KEY_SHOOT[self.name]] and self.shot_delay == 0:
            self.shot_fired = True  # <<< Flag que o tutorial usa
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]

            try:
                sound = AssetManager.get_sound(f"{self.name}Shot.mp3")
                sound.set_volume(0.5)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som de tiro] {e}")

            return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

        self.shot_fired = False  # <<< Zera a flag se não atirou
        return None

    def take_damage_flash(self):
        self.damage_flash_timer = 10
        if hasattr(self, "window") and hasattr(self, "particles"):
            self.particles.append(AuraBurstParticle(self.rect.center))

    def draw(self, surface):
        offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        angle = math.sin(pygame.time.get_ticks() * 0.002) * 5
        rotated = pygame.transform.rotate(self.image, angle)

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1

            mask = pygame.mask.from_surface(rotated)
            red_overlay = pygame.Surface(rotated.get_size(), pygame.SRCALPHA)

            for x in range(rotated.get_width()):
                for y in range(rotated.get_height()):
                    if mask.get_at((x, y)):
                        red_overlay.set_at((x, y), (255, 0, 0, 120))

            rotated.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        rect = rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
        surface.blit(rotated, rect)

    def update(self):
        self.move()

        shot = self.shoot()
        if shot:
            if hasattr(self, "particles"):
                self.particles.append(shot)
            elif hasattr(self, "entity_manager"):
                self.entity_manager.add_entity(shot)

        # Se não atirou neste frame, zera a flag (importante para o tutorial)
        if not shot:
            self.shot_fired = False

