import math
import random
import pygame
from code.system.entity import Entity
from code.system.particle import AmbientFloatParticle, MagicFogParticle, draw_grain_overlay
from code.CombatEntity.player import Player
from code.CombatEntity.enemy import Enemy
from code.DrawableEntity.MovingEntity.background import Background
from code.system.entitymediator import EntityMediator

class EntityManager:
    def __init__(self, entity_list: list[Entity], window: pygame.Surface):
        self.entity_list = entity_list
        self.window = window

        # Efeitos visuais mágicos
        self.enable_ambient_particles = False
        self.enable_magic_fog = False
        self.particles_ambient = []
        self.particles_fog = []
        self.particles_impact = []

    def update_entities(self):
        for ent in self.entity_list:
            if hasattr(ent, "update"):
                ent.update()  # ✅ Chama update do Player, Enemy, etc.

            elif hasattr(ent, "move"):
                ent.move()

            if isinstance(ent, (Player, Enemy)) or ent.name == "Boss":
                shot = ent.shoot()
                if shot:
                    self.entity_list.append(shot)

            if isinstance(ent, Player):
                if ent.damage_timer > 0:
                    ent.damage_timer -= 1
                else:
                    ent.damage_counter = 0

    def draw_backgrounds(self):
        # 1. Desenha todos os backgrounds normais
        for ent in self.entity_list:
            if isinstance(ent, Background):
                self.window.blit(ent.surf, ent.rect)

        # 2. Aplica a camada de luz por cima, com transparência animada
        for ent in self.entity_list:
            if ent.name.startswith("LightOverlay"):
                overlay = ent.surf.copy()
                alpha = 80 + int(20 * math.sin(pygame.time.get_ticks() * 0.002))
                overlay.set_alpha(alpha)
                self.window.blit(overlay, (0, 0))

    def draw_entities(self):
        for ent in self.entity_list:
            if hasattr(ent, "draw"):
                ent.draw(self.window)
            elif not isinstance(ent, Background) and not ent.name.startswith("LightOverlay"):
                self.window.blit(ent.image, ent.rect)

    def draw_particles(self):
        # Ambiente
        for p in self.particles_fog:
            p.draw(self.window)
        for p in self.particles_ambient:
            p.draw(self.window)
        for p in self.particles_impact:
            p.draw(self.window)

        # Partículas dos tiros e entidades
        for ent in self.entity_list:
            if hasattr(ent, "draw_particles"):
                ent.draw_particles(self.window)

        draw_grain_overlay(self.window)


    def handle_collisions(self):
        EntityMediator.verify_collision(self, self.entity_list)
        EntityMediator.verify_health(self, self.entity_list)

    def get_players(self):
        return [e for e in self.entity_list if isinstance(e, Player)]

    def is_player_alive(self):
        return any(isinstance(e, Player) for e in self.entity_list)

    def get_entities(self):
        return self.entity_list

    def add_entity(self, entity):
        self.entity_list.append(entity)

    def has_entity_named(self, name: str) -> bool:
        return any(entity.name == name for entity in self.get_entities())

    def update_visual_effects(self):
        # Partículas flutuantes
        if self.enable_ambient_particles:
            if len(self.particles_ambient) < 30:
                self.particles_ambient.append(AmbientFloatParticle(self.window.get_size()))
            for p in self.particles_ambient[:]:
                p.update()
                if p.lifetime <= 0:
                    self.particles_ambient.remove(p)

        # Névoa mágica
        if self.enable_magic_fog:
            if len(self.particles_fog) < 8:
                self.particles_fog.append(MagicFogParticle(self.window.get_size()))
            for p in self.particles_fog:
                p.update()

        # Impacto: já tratado nos próprios objetos
        for p in self.particles_impact[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles_impact.remove(p)

    def update_selected_entities(self, allowed_names: list[str]):
        for entity in self.entity_list:
            if (
                    (entity.name in allowed_names or entity.name.endswith("Shot") or entity.name.startswith("Level1Bg"))
                    and hasattr(entity, 'update')
            ):
                entity.update()

