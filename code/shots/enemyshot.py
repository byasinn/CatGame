import random
import pygame
from code.system.config import ENTITY_SPEED
from code.CombatEntity.combatentity import CombatEntity
from code.system.managers.assetmanager import AssetManager
from code.system.particle import Particle


class EnemyShot(CombatEntity):
    def __init__(self, name, position, direction=None):
        super().__init__(name, position)
        self.direction = direction or pygame.Vector2(-1, 0)
        self.speed = 8

        # Animação de 3 frames
        self.frames = [
            AssetManager.get_image(f"{name}1.png"),
            AssetManager.get_image(f"{name}2.png"),
            AssetManager.get_image(f"{name}3.png")
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 5

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

        # Partículas
        self.particles: list[Particle] = []

        # Personalização por tipo de inimigo
        if "Enemy1" in name:
            self.particle_color = (255, 100, 100)
            self.particle_size = (1, 3)
        elif "Enemy2" in name:
            self.particle_color = (255, 180, 80)
            self.particle_size = (2, 4)
        elif "Enemy3" in name:
            self.particle_color = (160, 200, 255)
            self.particle_size = (5, 8)
        else:
            self.particle_color = (255, 255, 200)
            self.particle_size = (1, 3)

    def update(self):
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

        # Animação
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.image = self.frames[self.current_frame]

        # Partículas
        offset = pygame.Vector2(-8 * self.direction.x, random.uniform(-2, 2))
        part = Particle(self.rect.center + offset)
        part.color = self.particle_color
        part.radius = random.randint(*self.particle_size)
        part.lifetime = random.randint(12, 22)
        self.particles.append(part)

        for p in self.particles:
            p.update()

        self.particles = [p for p in self.particles if p.lifetime > 0]

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_particles(self, surface):
        for p in self.particles:
            p.draw(surface)
