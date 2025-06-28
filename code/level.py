#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.background import Background
from code.const import MENU_OPTION, EVENT_ENEMY, EVENT_TIMEOUT, SPAWN_TIME, TIMEOUT_STEP, \
    TIMEOUT_LEVEL
from code.enemy import Enemy
from code.entitymanager import EntityManager
from code.player import Player
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.entitymediator import EntityMediator
from code.hud import HUDRenderer


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.window = window
        self.timeout = TIMEOUT_LEVEL
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + "Bg"))

        # Criar jogadores
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        # Criar HUD e EntityManager depois da lista de entidades estar completa
        self.hud = HUDRenderer(self.window)
        self.entity_manager = EntityManager(self.entity_list, self.window)

        self.boss_summoned = False
        self.boss_delay = 5000
        self.boss_timer = 0

        self.game_mode_str = {
            MENU_OPTION[0]: "Solo",
            MENU_OPTION[1]: "Coop",
            MENU_OPTION[2]: "Versus",
        }[game_mode]

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

            # --- DESENHO DOS OUTROS ELEMENTOS ---
            self.entity_manager.draw_backgrounds()
            self.entity_manager.draw_entities()
            self.entity_manager.draw_particles()
            self.entity_manager.update_entities()
            self.entity_manager.handle_collisions()
            players = self.entity_manager.get_players()

            # --- LUZ SOBRE O FUNDO ---
            sunlight_copy = self.sunlight.copy()
            sunlight_copy.set_alpha(80 + int(20 * math.sin(pygame.time.get_ticks() * 0.002)))
            self.window.blit(sunlight_copy, (0, 0))

            players_alive = self.entity_manager.is_player_alive()
            if not players_alive:
                return False  # fim do jogo


            # --- Chamada do HUD ---
            players = self.entity_manager.get_players()
            self.hud.draw_hud(
                players=players,
                level_name=self.name,
                timeout=self.timeout,
                boss_summoned=self.boss_summoned,
                fps=clock.get_fps(),
                entity_count=len(self.entity_manager.get_entities())
            )
            for p in self.entity_manager.get_players():
                if p.name == "Player1":
                    player_score[0] = p.score
                elif p.name == "Player2":
                    player_score[1] = p.score
            self.hud.draw_score(self.game_mode_str, player_score, pygame.time.get_ticks())

            # --- EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', "Enemy2"))
                    self.entity_manager.add_entity(EntityFactory.get_entity(choice))

                # No EVENT_TIMEOUT
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP

                    # Se o tempo acabou
                    if self.name == "Level3" and self.timeout <= 0 and not self.boss_summoned:
                        pygame.time.set_timer(EVENT_ENEMY, 0)
                        pygame.time.set_timer(EVENT_TIMEOUT, 0)
                        self.boss_summoned = True
                        self.entity_manager.add_entity(EntityFactory.get_entity("Boss"))

                    elif self.name in ["Level1", "Level2"] and self.timeout <= 0:
                        for p in self.entity_manager.get_players():
                            if p.name == "Player1":
                                player_score[0] = p.score
                            elif p.name == "Player2":
                                player_score[1] = p.score
                        return True

            # Se estiver na Level3 e o boss já foi invocado
            if self.name == "Level3" and self.boss_summoned:
                boss_alive = any(e.name == "Boss" and e.health > 0 for e in self.entity_list)
                if not boss_alive:
                    for p in self.entity_manager.get_players():
                        if p.name == "Player1":
                            player_score[0] = p.score
                        elif p.name == "Player2":
                            player_score[1] = p.score
                    return True

            pygame.display.flip()

    pass