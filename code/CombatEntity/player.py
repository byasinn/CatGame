#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random

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

        self.image_normal = AssetManager.get_image(f"{self.name}.png")
        self.image_blink = AssetManager.get_image(f"{self.name}_blink.png")

        self.image = self.image_normal  # atual
        self.blink_timer = 0
        self.blink_interval = random.randint(240, 360)  # 4~6s
        self.blink_duration = 5  # dura 5 frames (~0.08s)

        self.paw_frames = [
            AssetManager.get_image(f"{self.name}Paw1.png"),
            AssetManager.get_image(f"{self.name}Paw2.png"),
            AssetManager.get_image(f"{self.name}Paw3.png"),
            AssetManager.get_image(f"{self.name}Paw2.png")  # looping simétrico
        ]
        self.paw_frame_index = 0
        self.paw_frame_timer = 0

        self.tail_frames = [
            AssetManager.get_image(f"{self.name}Tail1.png"),
            AssetManager.get_image(f"{self.name}Tail2.png"),
            AssetManager.get_image(f"{self.name}Tail3.png"),
            AssetManager.get_image(f"{self.name}Tail2.png")  # Para voltar suavemente
        ]
        self.tail_frame_index = 0
        self.tail_frame_timer = 0
        self.blink_force = False

        self.current_angle = 0
        self.target_angle = 0

    def move(self):
        self.dir = 0  # parado por padrão

        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < self.window.get_height():
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
            self.dir = -1
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < self.window.get_width():
            self.rect.centerx += ENTITY_SPEED[self.name]
            self.dir = 1

    def shoot(self):
        pressed_key = pygame.key.get_pressed()

        # Diminui o delay de tiro
        if self.shot_delay > 0:
            self.shot_delay -= 1

        # Verifica se pode atirar
        if pressed_key[PLAYER_KEY_SHOOT[self.name]] and self.shot_delay == 0:
            self.blink_force = True
            self.image = self.image_blink
            self.blink_timer = 0

            self.shot_fired = True
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]

            try:
                sound = AssetManager.get_sound(f"{self.name}Shot.mp3")
                sound.set_volume(0.5)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som de tiro] {e}")

            offset_y = -20 if self.name == "Player2" else 10
            spawn_x = self.rect.centerx + 30
            spawn_y = self.rect.centery + offset_y

            return PlayerShot(name=f'{self.name}Shot', position=(spawn_x, spawn_y))

        self.shot_fired = False
        return None

    def take_damage_flash(self):
        self.damage_flash_timer = 10  # efeito de flash

        if hasattr(self, "window") and hasattr(self, "particles"):
            self.particles.append(AuraBurstParticle(self.rect.center))

    def apply_damage_flash(self, surface):
        if self.damage_flash_timer > 0:
            # Cria uma máscara para preservar apenas os pixels visíveis (não transparentes)
            mask = pygame.mask.from_surface(surface)
            red_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

            for x in range(surface.get_width()):
                for y in range(surface.get_height()):
                    if mask.get_at((x, y)):
                        red_overlay.set_at((x, y), (255, 0, 0, 120))

            surface.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def draw(self, surface):
        offset = math.sin(pygame.time.get_ticks() * 0.005) * 2

        base_angle = math.sin(pygame.time.get_ticks() * 0.002) * 3
        if self.dir == 1:
            self.target_angle = -8
        elif self.dir == -1:
            self.target_angle = 8
        else:
            self.target_angle = 0
        self.current_angle += (self.target_angle - self.current_angle) * 0.2
        angle = base_angle + self.current_angle

        rotated = pygame.transform.rotate(self.image, angle)

        # Patinha animada sobre o corpo
        paw = self.current_paw_frame
        paw_rotated = pygame.transform.rotate(paw, angle)
        paw_rect = paw_rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
        self.apply_damage_flash(paw_rotated)
        surface.blit(paw_rotated, paw_rect)

        # Cauda animada
        tail = self.tail_frames[self.tail_frame_index]
        tail_rotated = pygame.transform.rotate(tail, angle)
        tail_rect = tail_rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
        self.apply_damage_flash(tail_rotated)
        surface.blit(tail_rotated, tail_rect)

        self.apply_damage_flash(rotated)
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1

        rect = rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
        surface.blit(rotated, rect)

    def update(self):
        self.move()
        self.update_tail_animation()
        self.update_blink_animation()
        self.update_paw_animation()

        shot = self.shoot()
        if shot:
            if hasattr(self, "particles"):
                self.particles.append(shot)
            elif hasattr(self, "entity_manager"):
                self.entity_manager.add_entity(shot)

        # Se não atirou neste frame, zera a flag (importante para o tutorial)
        if not shot:
            self.shot_fired = False

    def update_blink_animation(self):
        self.blink_timer += 1

        # Caso seja uma piscada forçada (por tiro)
        if self.blink_force:
            if self.blink_timer >= self.blink_duration:
                self.image = self.image_normal
                self.blink_force = False
                self.blink_timer = 0
            return  # não interfere com o ciclo natural

        # Piscada automática normal
        if self.blink_timer == self.blink_interval:
            self.image = self.image_blink

        elif self.blink_timer == self.blink_interval + self.blink_duration:
            self.image = self.image_normal
            self.blink_timer = 0
            self.blink_interval = random.randint(240, 360)

    def update_paw_animation(self):
        # Sequência da animação
        paw_sequence = [2, 3, 2, 1, 2, 3, 2]  # nomes: Paw2, Paw3, ...
        frame_delay = 10  # quantos frames entre cada troca
        pause_delay = 100  # 2 segundos se rodando a 60fps
        self.paw_frame_timer += 1

        # Verifica se é hora de trocar
        current_delay = pause_delay if self.paw_frame_index == len(paw_sequence) - 1 else frame_delay

        if self.paw_frame_timer >= current_delay:
            self.paw_frame_timer = 0
            self.paw_frame_index = (self.paw_frame_index + 1) % len(paw_sequence)

        # Aponta para o frame atual
        frame = paw_sequence[self.paw_frame_index]
        self.current_paw_frame = self.paw_frames[frame - 1]  # index de nome: Paw1 → [0]

    def update_tail_animation(self):
        self.tail_frame_timer += 1
        if self.tail_frame_timer >= 10:  # Troca a cada 6 frames (~10x por segundo)
            self.tail_frame_index = (self.tail_frame_index + 1) % len(self.tail_frames)
            self.tail_frame_timer = 0
