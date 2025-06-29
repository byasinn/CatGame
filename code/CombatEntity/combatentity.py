from code.DrawableEntity.drawableentity import DrawableEntity
from code.const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE

class CombatEntity(DrawableEntity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.health = ENTITY_HEALTH[name]
        self.damage = ENTITY_DAMAGE[name]
        self.score = ENTITY_SCORE[name]
        self.last_dmg = "None"

    def take_damage(self, amount: int):
        self.health -= amount
