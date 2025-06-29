import random

import pygame
from code.const import EVENT_ENEMY, EVENT_TIMEOUT, SPAWN_TIME, TIMEOUT_STEP, TIMEOUT_LEVEL


class TimerController:
    def __init__(self, level_name: str):
        self.timeout = TIMEOUT_LEVEL
        self.level_name = level_name
        self.boss_summoned = False


        # Inicia os timers do pygame
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def update(self, event_list, entity_list, entity_factory):
        """
        Processa eventos de tempo.
        Retorna:
        - 'boss' se o boss foi invocado
        - 'complete' se a fase terminou
        - None caso contrário
        """
        for event in event_list:
            if event.type == EVENT_TIMEOUT:
                self.timeout -= TIMEOUT_STEP

                if self.level_name == "Level3" and self.timeout <= 0 and not self.boss_summoned:
                    pygame.time.set_timer(EVENT_ENEMY, 0)
                    pygame.time.set_timer(EVENT_TIMEOUT, 0)
                    self.boss_summoned = True
                    entity_list.append(entity_factory.get_entity("Boss"))
                    return "boss"

                elif self.level_name in ["Level1", "Level2"] and self.timeout <= 0:
                    return "complete"

        return None

    def get_timeout(self):
        return self.timeout

    def has_boss(self):
        return self.boss_summoned

class ArcadeTimerController:

    def __init__(self):
        self.spawn_timer = 3000
        self.speed_increment_timer = 10000
        self.last_spawn = pygame.time.get_ticks()
        self.last_speedup = pygame.time.get_ticks()
        self.difficulty_level = 1
        self.max_difficulty = 5

    def update(self, event_list, entity_list, entity_factory):
        now = pygame.time.get_ticks()

        if now - self.last_spawn > self.spawn_timer:
            self.last_spawn = now
            entity_list.append(entity_factory.get_entity(random.choice(["Enemy1", "Enemy2"])))

        if now - self.last_speedup > self.speed_increment_timer:
            self.last_speedup = now
            self.difficulty_level = min(self.difficulty_level + 1, self.max_difficulty)

        # exemplo: aumentar a velocidade global
        from code.const import ENTITY_SPEED
        for name in ["Enemy1", "Enemy2"]:
            ENTITY_SPEED[name] = min(ENTITY_SPEED[name] + 1, 6)

    def get_timeout(self):
        return 99999

    def has_boss(self):
        return False  # nunca terá boss no arcade
