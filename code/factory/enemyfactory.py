import pygame
import random
from code.CombatEntity.enemy import Enemy
from code.CombatEntity.boss import Boss

class EnemyFactory:
    @staticmethod
    def create(enemy_type: str):
        surface = pygame.display.get_surface()
        x = surface.get_width() + 10
        y = random.randint(30, surface.get_height() - 30)

        if enemy_type == "Boss":
            return Boss("Boss", (x, y), surface)
        else:
            return Enemy(enemy_type, (x, y), surface)
