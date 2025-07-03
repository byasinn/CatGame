import math
import pygame
import random

from code.system.managers.assetmanager import AssetManager
from code.system.config import ENTITY_SHOT_DELAY, ENTITY_SPEED
from code.shots.enemyshot import EnemyShot
from code.CombatEntity.combatentity import CombatEntity

class Boss(CombatEntity):
    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
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
                random.randint(self.window.get_width() // 2, self.window.get_width() - 60),
                random.randint(30, self.window.get_height() - 30)
            ]
            self.move_cooldown = 60

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
            try:
                sound = AssetManager.get_sound("BossShot.mp3")
                sound.set_volume(0.5)
                sound.play()
            except Exception as e:
                print(f"[Erro ao tocar som do Boss] {e}")

            return EnemyShot(name=f"{self.name}Shot", position=(self.rect.centerx, self.rect.centery))
        return None

    def draw(self, surface):
        offset = math.sin(pygame.time.get_ticks() * 0.004) * 2
        angle = math.sin(pygame.time.get_ticks() * 0.0025) * 4
        rotated = pygame.transform.rotate(self.image, angle)

        rect = rotated.get_rect(center=(self.rect.centerx, self.rect.centery + offset))
        surface.blit(rotated, rect)