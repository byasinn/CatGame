#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.background import Background
from code.const import WIN_HEIGHT, COLOR_WHITE, MENU_OPTION, EVENT_ENEMY, EVENT_TIMEOUT, SPAWN_TIME, TIMEOUT_STEP, \
    TIMEOUT_LEVEL
from code.enemy import Enemy
from code.player import Player
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.entitymediator import EntityMediator


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.window = window
        self.timeout = TIMEOUT_LEVEL
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + "Bg"))
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)
        if game_mode in [MENU_OPTION[1],MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        self.boss_summoned = False
        self.boss_delay = 5000  # 5 segundos em ms
        self.boss_timer = 0

        if self.name == "Level1":
            self.sunlight = pygame.image.load("./asset/LightOverlay_Level1.png").convert_alpha()
        elif self.name == "Level2":
            self.sunlight = pygame.image.load("./asset/LightOverlay_Level2.png").convert_alpha()
        elif self.name == "Level3":
            self.sunlight = pygame.image.load("./asset/LightOverlay_Level2.png").convert_alpha()

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)


    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.boss_timer += clock.get_time()

            # --- FUNDO ---
            for ent in self.entity_list:
                if isinstance(ent, Background):
                    self.window.blit(ent.surf, ent.rect)

            # --- DESENHO DOS OUTROS ELEMENTOS ---
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
                    angle = math.sin(pygame.time.get_ticks() * 0.002) * 5
                    surf = pygame.transform.rotate(ent.surf, angle)

                    if ent.damage_flash_timer > 0:
                        ent.damage_flash_timer -= 1
                        red_overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                        red_overlay.fill((255, 0, 0, 120))  # vermelho semi-transparente
                        surf.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

                    rect = surf.get_rect(center=(ent.rect.centerx, ent.rect.centery + offset))
                    self.window.blit(surf, rect)

                elif not isinstance(ent, Background) and not ent.name.startswith("LightOverlay"):
                    self.window.blit(ent.surf, ent.rect)


            # --- MOVIMENTO E TIROS ---
            for ent in self.entity_list:
                ent.move()
                if isinstance(ent, (Player, Enemy)) or ent.name == "Boss":
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            # --- LUZ SOBRE O FUNDO ---
            sunlight_copy = self.sunlight.copy()
            sunlight_copy.set_alpha(80 + int(20 * math.sin(pygame.time.get_ticks() * 0.002)))
            self.window.blit(sunlight_copy, (0, 0))

            # Desenhar partículas dos tiros
            for ent in self.entity_list:
                if hasattr(ent, "draw_particles"):
                    ent.draw_particles(self.window)

            # --- HUD ---
            for ent in self.entity_list:
                if ent.name == "Player1":
                    self.level_text(14, f'Mora - Health: {ent.health} | Score: {ent.score}', COLOR_WHITE, (10, 25))
                if ent.name == "Player2":
                    self.level_text(14, f'Leon - Health: {ent.health} | Score: {ent.score}', COLOR_WHITE, (10, 45))

            if not (self.name == "Level3" and self.boss_summoned):
                self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000 : .1f}s', COLOR_WHITE, (10, 5))

            self.level_text(14, f'fps: {clock.get_fps() :.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(24, f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))

            players_alive = any(isinstance(ent, Player) for ent in self.entity_list)
            if not players_alive:
                return False  # fim do jogo


            pygame.display.flip()

            # --- EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', "Enemy2"))
                    self.entity_list.append(EntityFactory.get_entity(choice))

                # No EVENT_TIMEOUT
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP

                    # Se o tempo acabou
                    if self.name == "Level3" and self.timeout <= 0 and not self.boss_summoned:
                        pygame.time.set_timer(EVENT_ENEMY, 0)
                        pygame.time.set_timer(EVENT_TIMEOUT, 0)
                        self.boss_summoned = True
                        self.entity_list.append(EntityFactory.get_entity("Boss"))

                    elif self.name in ["Level1", "Level2"] and self.timeout <= 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True

            # --- VERIFICA MORTE E COLISÕES ---
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

            # Se estiver na Level3 e o boss já foi invocado
            if self.name == "Level3" and self.boss_summoned:
                boss_alive = any(e.name == "Boss" and e.health > 0 for e in self.entity_list)
                if not boss_alive:
                    for ent in self.entity_list:
                        if isinstance(ent, Player) and ent.name == 'Player1':
                            player_score[0] = ent.score
                        if isinstance(ent, Player) and ent.name == 'Player2':
                            player_score[1] = ent.score
                    return True

    pass

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)