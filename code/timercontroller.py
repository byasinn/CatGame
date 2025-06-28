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