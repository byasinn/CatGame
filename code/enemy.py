#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.const import ENTITY_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY, WIN_HEIGHT
from code.enemyshot import EnemyShot
from code.entity import Entity


class Enemy(Entity):

    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        if self.name == "Enemy2":
            self.zigzag_timer = 0
            self.zigzag_direction = 0

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

        if self.name == "Enemy2":
            # Zigzag vertical aleatório
            if self.zigzag_timer > 0:
                next_y = self.rect.centery + self.zigzag_direction * 2

                # Limites da tela (com margem)
                if 30 < next_y < WIN_HEIGHT - 30:
                    self.rect.centery = next_y

                self.zigzag_timer -= 1
            else:
                # 30% de chance de iniciar zigzag
                if random.random() < 0.3:
                    self.zigzag_direction = random.choice([-1, 1])
                    self.zigzag_timer = random.randint(20, 60)
                else:
                    self.zigzag_direction = 0

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]

            # Som do tiro do inimigo
            try:
                sound = pygame.mixer.Sound(f"./asset/{self.name}Shot.mp3")
                sound.set_volume(0.4)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som de {self.name}] {e}")

            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        return None