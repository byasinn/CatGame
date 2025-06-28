#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.background import Background
from code.const import MENU_OPTION, EVENT_ENEMY
from code.entitymanager import EntityManager
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.hud import HUDRenderer
from code.timercontroller import TimerController
from code.eventcontroller import EventController

class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.window = window
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

        # Componentes do jogo
        self.entity_manager = EntityManager(self.entity_list, self.window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(self.window)
        self.timer = TimerController(self.name)

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


    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        self.entity_manager.enable_ambient_particles = True
        self.entity_manager.enable_magic_fog = True

        for ent in self.entity_list:
            if ent.name.startswith("LightOverlay"):
                raw = pygame.image.load(f"./asset/{ent.name}.png").convert_alpha()
                w, h = self.window.get_size()
                ent.surf = pygame.transform.scale(raw, (w, h))

        while True:
            clock.tick(60)

            # Eventos
            event_list = pygame.event.get()
            self.event_controller.handle(event_list)
            event_result = self.timer.update(event_list, self.entity_manager.get_entities(), EntityFactory)

            # Timeout completou
            if event_result == "complete":
                for p in self.entity_manager.get_players():
                    if p.name == "Player1":
                        player_score[0] = p.score
                    elif p.name == "Player2":
                        player_score[1] = p.score
                return True

            # Render & update
            self.entity_manager.draw_backgrounds()
            self.entity_manager.draw_entities()
            self.entity_manager.draw_particles()
            self.entity_manager.update_entities()
            self.entity_manager.update_visual_effects()
            self.entity_manager.handle_collisions()

            # Verifica fim de jogo
            if not self.entity_manager.is_player_alive():
                return False

            # HUD
            players = self.entity_manager.get_players()
            self.hud.draw_hud(
                players=players,
                level_name=self.name,
                timeout=self.timer.get_timeout(),
                boss_summoned=self.timer.has_boss(),
                fps=clock.get_fps(),
                entity_count=len(self.entity_manager.get_entities())
            )
            for p in players:
                if p.name == "Player1":
                    player_score[0] = p.score
                elif p.name == "Player2":
                    player_score[1] = p.score
            self.hud.draw_score(self.game_mode_str, player_score, pygame.time.get_ticks())

            # Vitória do jogador se boss morreu
            if self.name == "Level3" and self.timer.has_boss():
                boss_alive = any(e.name == "Boss" and e.health > 0 for e in self.entity_manager.get_entities())
                if not boss_alive:
                    for p in players:
                        if p.name == "Player1":
                            player_score[0] = p.score
                        elif p.name == "Player2":
                            player_score[1] = p.score
                    return True

            pygame.display.flip()
