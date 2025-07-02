#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import pygame

from code.system.assetmanager import AssetManager
from code.system.config import ENTITY_SPEED, ENTITY_SHOT_DELAY
from code.shots.enemyshot import EnemyShot
from code.CombatEntity.combatentity import CombatEntity

class Enemy(CombatEntity):
    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

        if self.name == "Enemy1":
            self.anim_frames = [
                AssetManager.get_image("Enemy1_1.png"),
                AssetManager.get_image("Enemy1_2.png"),
                AssetManager.get_image("Enemy1_3.png")
            ]
            self.anim_index = 0
            self.anim_timer = 0

        if self.name == "Enemy2":
            self.zigzag_timer = 0
            self.zigzag_direction = 0

    def move(self):
        if getattr(self, 'frozen', False):
            return

        self.rect.centerx -= ENTITY_SPEED[self.name]

        if self.name == "Enemy2":
            if self.zigzag_timer > 0:
                next_y = self.rect.centery + self.zigzag_direction * 2
                if 30 < next_y < self.window.get_height() - 30:
                    self.rect.centery = next_y
                self.zigzag_timer -= 1
            else:
                if random.random() < 0.3:
                    self.zigzag_direction = random.choice([-1, 1])
                    self.zigzag_timer = random.randint(20, 60)
                else:
                    self.zigzag_direction = 0

    def update(self):
        self.move()

        if self.name == "Enemy1":
            self.anim_timer += 1
            if self.anim_timer >= 10:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.anim_frames)

    def shoot(self):
        if getattr(self, 'frozen', False):
            return None

        self.shot_delay -= 1
        if self.shot_delay <= 0:
            if self.name == "Enemy1":
                self.shot_delay = random.randint(70, 130)
            else:
                self.shot_delay = ENTITY_SHOT_DELAY[self.name]

            try:
                sound = AssetManager.get_sound(f"{self.name}Shot.mp3")
                sound.set_volume(0.4)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som de {self.name}] {e}")

            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

        return None

    def draw(self, surface):
        if self.name == "Enemy2":
            offset = math.sin(pygame.time.get_ticks() * 0.005 + self.rect.x * 0.01) * 1.5
            angle = math.sin(pygame.time.get_ticks() * 0.002 + self.rect.x * 0.01) * 3
            rotated = pygame.transform.rotate(self.surf, angle)
            rect = rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
            surface.blit(rotated, rect)

        elif self.name == "Enemy1":
            surface.blit(self.surf, self.rect)  # hitbox invisível
            frame = self.anim_frames[self.anim_index]
            anim_rect = frame.get_rect(center=self.rect.center)
            surface.blit(frame, anim_rect)

        else:
            # fallback para qualquer outro tipo
            surface.blit(self.surf, self.rect)

