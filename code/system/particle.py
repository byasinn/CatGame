import pygame
import random

from code.system.assetmanager import AssetManager


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




# ✨ Partículas flutuantes mágicas
class AmbientFloatParticle:
    def __init__(self, window_size):
        self.x = random.randint(0, window_size[0])
        self.y = random.randint(0, window_size[1])
        self.radius = random.randint(1, 2)
        self.alpha = random.randint(50, 150)
        self.vel_y = random.uniform(-0.1, -0.4)
        self.lifetime = random.randint(300, 800)

    def update(self):
        self.y += self.vel_y
        self.alpha = max(0, self.alpha - 0.05)
        self.lifetime -= 1

    def draw(self, surface):
        if self.alpha > 0:
            glow = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 200, int(self.alpha)), (self.radius*2, self.radius*2), self.radius)
            surface.blit(glow, (self.x, self.y))

# 🌫 Névoa mágica
import pygame
import random
import math

class MagicFogParticle:
    def __init__(self, window_size):
        self.x = random.randint(0, window_size[0])
        self.y = random.randint(0, window_size[1])
        self.base_radius = random.randint(60, 120)
        self.alpha = random.randint(20, 35)
        self.vel_x = random.uniform(-0.3, 0.3)
        self.vel_y = random.uniform(-0.1, 0.1)
        self.color = random.choice([
            (200, 170, 255),
            (180, 220, 255),
            (255, 220, 255),
        ])
        self.time_offset = random.uniform(0, 1000)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Rebote
        win = pygame.display.get_surface().get_size()
        if self.x < -self.base_radius: self.x = win[0]
        if self.x > win[0]: self.x = -self.base_radius
        if self.y < -self.base_radius: self.y = win[1]
        if self.y > win[1]: self.y = -self.base_radius

    def draw(self, surface):
        t = pygame.time.get_ticks() / 1000 + self.time_offset
        pulsar = math.sin(t * 1.5) * 0.1 + 1  # ~90% a 110%
        radius = int(self.base_radius * pulsar)

        fog = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(fog, (*self.color, self.alpha), (radius, radius), radius)
        surface.blit(fog, (self.x, self.y))

class AuraBurstParticle:
    def __init__(self, position, color=(255, 255, 255)):
        self.pos = position
        self.radius = 20
        self.max_radius = 80
        self.color = color
        self.alpha = 255
        self.lifetime = 20

    def update(self):
        self.radius += 5
        self.alpha = max(0, self.alpha - 20)
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0 and self.alpha > 0:
            glow = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow,
                (*self.color, int(self.alpha)),
                (self.radius, self.radius),
                self.radius,
                width=3
            )
            surface.blit(glow, (self.pos[0] - self.radius, self.pos[1] - self.radius))



class ImpactParticle:
    def __init__(self, position, color=(180, 0, 0)):
        self.pos = list(position)
        self.vel = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.radius = random.randint(2, 4)
        self.color = color
        self.alpha = 255
        self.lifetime = 20

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.radius = max(0, self.radius - 0.1)
        self.alpha -= 10
        self.lifetime -= 1

    def draw(self, surface):
        if self.radius > 0 and self.alpha > 0:
            glow = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.color, int(self.alpha)), (self.radius*2, self.radius*2), int(self.radius))
            surface.blit(glow, (self.pos[0] - self.radius*2, self.pos[1] - self.radius*2))



grain_frames = []
grain_index = 0
grain_loaded = False
grain_frame_timer = 0
grain_frame_delay = 2  # muda a cada 2 frames (ajuste conforme quiser)

def draw_grain_overlay(surface):
    global grain_frames, grain_index, grain_loaded, grain_frame_timer

    if not grain_loaded:
        from code.system.assetmanager import AssetManager
        grain_frames = [AssetManager.get_image(f"grain_{i}.png").convert_alpha() for i in range(4)]
        grain_loaded = True

    # ⏱️ Controle de tempo entre trocas
    grain_frame_timer += 1
    if grain_frame_timer >= grain_frame_delay:
        grain_index = (grain_index + 1) % len(grain_frames)
        grain_frame_timer = 0

    # Blit do grão atual
    grain = grain_frames[grain_index]
    if not hasattr(draw_grain_overlay, "grain_scaled"):
        draw_grain_overlay.grain_scaled = [
            pygame.transform.scale(frame, surface.get_size()) for frame in grain_frames
        ]

    grain.set_alpha(5)  # ajuste a intensidade aqui
    surface.blit(grain, (0, 0))



