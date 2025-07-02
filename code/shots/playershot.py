from code.system.assetmanager import AssetManager
from code.system.config import ENTITY_SPEED
from code.system.particle import Particle
from code.CombatEntity.combatentity import CombatEntity

class PlayerShot(CombatEntity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.particles: list[Particle] = []

        # 🔹 Carregar os frames da animação do tiro
        self.frames = [
            AssetManager.get_image(f"{name}1.png"),
            AssetManager.get_image(f"{name}2.png"),
            AssetManager.get_image(f"{name}3.png"),
            AssetManager.get_image(f"{name}4.png")
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 5  # troca a cada 5 frames (~12 FPS)

        # 🔹 Começa com a primeira imagem e define o centro
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

    def move(self):
        self.rect.centerx += ENTITY_SPEED[self.name]

        # Centraliza visualmente embaixo do sprite do tiro
        adjusted_center = (self.rect.centerx, self.rect.centery + 4)
        self.particles.append(Particle(adjusted_center))

        # Atualiza partículas
        for p in self.particles:
            p.update()

        self.particles = [p for p in self.particles if p.lifetime > 0]

        # Animação do tiro
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.image = self.frames[self.current_frame]

    def draw_particles(self, surface):
        for p in self.particles:
            p.draw(surface)
