from code.system.config import ENTITY_SPEED
from code.system.particle import Particle
from code.CombatEntity.combatentity import CombatEntity

class PlayerShot(CombatEntity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.particles: list[Particle] = []

    def move(self):
        self.rect.centerx += ENTITY_SPEED[self.name]

        # Adiciona uma partícula na posição atual do tiro
        self.particles.append(Particle(self.rect.center))

        # Atualiza partículas
        for p in self.particles:
            p.update()

        # Remove partículas que já "morreram"
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw_particles(self, surface):
        for p in self.particles:
            p.draw(surface)
