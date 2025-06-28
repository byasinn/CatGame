import math
import pygame
from code.entity import Entity
from code.player import Player
from code.enemy import Enemy
from code.background import Background
from code.entitymediator import EntityMediator

class EntityManager:
    def __init__(self, entity_list: list[Entity], window: pygame.Surface):
        self.entity_list = entity_list
        self.window = window

    def update_entities(self):
        for ent in self.entity_list:
            ent.move()
            if isinstance(ent, (Player, Enemy)) or ent.name == "Boss":
                shot = ent.shoot()
                if shot:
                    self.entity_list.append(shot)

    def draw_backgrounds(self):
        for ent in self.entity_list:
            if isinstance(ent, Background):
                self.window.blit(ent.surf, ent.rect)

    def draw_entities(self):
        for ent in self.entity_list:
            if isinstance(ent, Player):
                offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
                angle = math.sin(pygame.time.get_ticks() * 0.002) * 5
                surf = pygame.transform.rotate(ent.surf, angle)

                if ent.damage_flash_timer > 0:
                    ent.damage_flash_timer -= 1
                    red_overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                    red_overlay.fill((255, 0, 0, 120))
                    surf.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

                rect = surf.get_rect(center=(ent.rect.centerx, ent.rect.centery + offset))
                self.window.blit(surf, rect)

            elif not isinstance(ent, Background) and not ent.name.startswith("LightOverlay"):
                self.window.blit(ent.surf, ent.rect)

    def draw_particles(self):
        for ent in self.entity_list:
            if hasattr(ent, "draw_particles"):
                ent.draw_particles(self.window)

    def handle_collisions(self):
        EntityMediator.verify_collision(self.entity_list)
        EntityMediator.verify_health(self.entity_list)

    def get_players(self):
        return [e for e in self.entity_list if isinstance(e, Player)]

    def is_player_alive(self):
        return any(isinstance(e, Player) for e in self.entity_list)

    def get_entities(self):
        return self.entity_list

    def add_entity(self, entity):
        self.entity_list.append(entity)