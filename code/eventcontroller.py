import random
import sys
import pygame
from code.const import EVENT_ENEMY


class EventController:
    def __init__(self, entity_manager, entity_factory):
        self.entity_manager = entity_manager
        self.entity_factory = entity_factory

    def handle(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == EVENT_ENEMY:
                choice = random.choice(('Enemy1', "Enemy2"))
                enemy = self.entity_factory.get_entity(choice)
                self.entity_manager.add_entity(enemy)