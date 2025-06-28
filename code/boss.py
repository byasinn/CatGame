from code.entity import Entity
from code.enemyshot import EnemyShot
from code.const import ENTITY_SHOT_DELAY, ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH

import pygame
import random

class Boss(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.direction = 1  # 1 = descendo, -1 = subindo

    def move(self):
        if not hasattr(self, 'target_pos'):
            self.target_pos = [self.rect.centerx - 100, self.rect.centery]
            self.move_cooldown = 0

        self.move_cooldown -= 1
        if self.move_cooldown <= 0:
            # Novo destino aleatório dentro da tela
            self.target_pos = [
                random.randint(WIN_WIDTH // 2, WIN_WIDTH - 60),
                random.randint(30, WIN_HEIGHT - 30)
            ]
            self.move_cooldown = 60  # frames até trocar de novo

        # Movimento suave
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        if abs(dx) > 2:
            self.rect.centerx += int(dx / abs(dx)) * ENTITY_SPEED[self.name]
        if abs(dy) > 2:
            self.rect.centery += int(dy / abs(dy)) * ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay <= 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f"{self.name}Shot", position=(self.rect.centerx, self.rect.centery))
        return None
