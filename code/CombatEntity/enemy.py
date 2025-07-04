#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import pygame
from code.system.managers.assetmanager import AssetManager
from code.system.config import ENTITY_SPEED, ENTITY_SHOT_DELAY
from code.shots.enemyshot import EnemyShot
from code.CombatEntity.combatentity import CombatEntity

class Enemy(CombatEntity):
    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
        self.name = name
        self.health = 100
        self.speed = 3.5
        self.damage = 10
        self.shot_delay = ENTITY_SHOT_DELAY.get(name, 60)
        self.anim_index = 0
        self.anim_timer = 0

        if name == "EnemyTest":
            self.surf = AssetManager.get_image("EnemyTest.png")
            self.rect = self.surf.get_rect(center=position)
            self.anim_frames = [
                AssetManager.get_image("EnemyTest_1.png"),
                AssetManager.get_image("EnemyTest_2.png"),
                AssetManager.get_image("EnemyTest_3.png")
            ]

        if name == "Enemy1":
            self.surf = AssetManager.get_image("Enemy1.png")
            self.rect = self.surf.get_rect(center=position)
            self.anim_frames = [
                AssetManager.get_image("Enemy1_1.png"),
                AssetManager.get_image("Enemy1_2.png"),
                AssetManager.get_image("Enemy1_3.png")
            ]

        elif name == "Enemy2":
            self.surf = AssetManager.get_image("Enemy2.png")
            self.rect = self.surf.get_rect(center=position)
            self.zigzag_timer = 0
            self.zigzag_direction = 0
            self.anim_frames = [
                AssetManager.get_image("Enemy2_1.png"),
                AssetManager.get_image("Enemy2_2.png"),
                AssetManager.get_image("Enemy2_3.png")
            ]


        elif name == "Enemy3":
            self.surf = AssetManager.get_image("Enemy3.png")
            self.rect = self.surf.get_rect(center=position)
            self.anim_frames = [
                AssetManager.get_image("Enemy3_1.png"),
                AssetManager.get_image("Enemy3_2.png"),
                AssetManager.get_image("Enemy3_3.png")
            ]
            self.health = 110
            self.damage = 12
            self.speed = 2.0
            self.score = 150
            self.last_shot_time = pygame.time.get_ticks()
            self.shot_delay = random.randint(1000, 1800)
            self.behavior_timer = 0
            self.state = "moving"

        # 🔒 Proteção contra inimigos com nome desconhecido (ex: "EnemyTest")
        if not hasattr(self, "anim_frames"):
            self.surf = AssetManager.get_image("EnemyFallback.png")  # imagem transparente ou debug
            self.rect = self.surf.get_rect(center=position)
            self.anim_frames = [self.surf]

    def move(self):
        if getattr(self, 'frozen', False):
            return

        if self.name == "Enemy2":
            self.rect.centerx -= ENTITY_SPEED[self.name]
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

        elif self.name == "Enemy3":
            if self.state == "moving":
                self.rect.centerx -= self.speed
                self.behavior_timer += 1
                if self.behavior_timer > 180:
                    self.state = "idle"
                    self.behavior_timer = 0
            elif self.state == "idle":
                self.behavior_timer += 1
                if self.behavior_timer > 120:
                    self.state = "moving"
                    self.behavior_timer = 0

        else:
            self.rect.centerx -= ENTITY_SPEED.get(self.name, 1)

    def update(self):
        self.move()
        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.anim_frames)

        shot = self.shoot()
        if shot and hasattr(self, "entity_manager"):
            self.entity_manager.add_entity(shot)

    def shoot(self):
        if self.name == "Enemy3":
            now = pygame.time.get_ticks()
            if now - self.last_shot_time >= self.shot_delay:
                self.last_shot_time = now
                self.shot_delay = random.randint(1000, 1800)
                players = self.entity_manager.get_players() if hasattr(self, "entity_manager") else []
                if not players:
                    return None
                target = min(players, key=lambda p: abs(p.rect.centery - self.rect.centery))
                direction = pygame.Vector2(-1, target.rect.centery - self.rect.centery).normalize()
                return EnemyShot(name="Enemy3Shot", position=self.rect.center, direction=direction)
            return None

        # Enemy1 ou Enemy2 ou outros padrões
        self.shot_delay -= 1
        if self.shot_delay <= 0:
            if self.name == "Enemy1":
                self.shot_delay = random.randint(30, 40)
            elif self.name == "Enemy2":
                self.shot_delay = random.randint(45, 60)
            else:
                self.shot_delay = random.randint(35, 80)  # padrão para outros, como EnemyTest

            try:
                sound = AssetManager.get_sound(f"{self.name}Shot.mp3")
                sound.set_volume(0.4)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som de {self.name}] {e}")

            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

        return None

    def draw(self, surface):
        if not hasattr(self, "anim_frames"):
            surface.blit(self.surf, self.rect)
            return

        frame = self.anim_frames[self.anim_index]

        if self.name == "Enemy2":
            offset = math.sin(pygame.time.get_ticks() * 0.005 + self.rect.x * 0.01) * 1.5
            angle = math.sin(pygame.time.get_ticks() * 0.002 + self.rect.x * 0.01) * 3
            rotated = pygame.transform.rotate(frame, angle)
            rect = rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
            surface.blit(rotated, rect)

        elif self.name == "Enemy3":
            offset = math.sin(pygame.time.get_ticks() * 0.004 + self.rect.x * 0.015) * 2
            angle = math.sin(pygame.time.get_ticks() * 0.003 + self.rect.x * 0.012) * 3
            rotated = pygame.transform.rotate(frame, angle)
            rect = rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
            surface.blit(rotated, rect)

        else:
            anim_rect = frame.get_rect(center=self.rect.center)
            surface.blit(self.surf, self.rect)
            surface.blit(frame, anim_rect)

