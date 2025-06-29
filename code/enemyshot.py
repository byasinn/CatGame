from code.const import ENTITY_SPEED
from code.CombatEntity.combatentity import CombatEntity


class EnemyShot(CombatEntity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
