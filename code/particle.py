import pygame
import random

class Particle:
    def __init__(self, position):
        self.pos = list(position)
        self.radius = random.randint(1, 3)
        self.color = (255, 255, 150)
        self.lifetime = random.randint(10, 20)

    def update(self):
        self.pos[0] += random.uniform(-0.5, 0.5)
        self.pos[1] += random.uniform(-1, 1)
        self.radius -= 0.1
        self.lifetime -= 1

    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))
