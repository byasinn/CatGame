import pygame
from code.entitybase import Entity
from code.const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE

class DrawableEntity(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name)
        self.image = pygame.image.load(f'./asset/{name}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
