#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.settings.settingsmanager import SettingsManager
from code.assetmanager import AssetManager
from code.background import Background
from code.const import MENU_OPTION, EVENT_ENEMY
from code.entitymanager import EntityManager
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.hud import HUDRenderer
from code.timercontroller import TimerController, ArcadeTimerController
from code.eventcontroller import EventController

class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int], is_arcade=False, audio=None):

        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.is_arcade = is_arcade
        self.audio = audio

        # Criar jogadores
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        if self.is_arcade:
            self.entity_list.extend(EntityFactory.get_entity("Level1Bg"))
            self.timer = ArcadeTimerController()
        else:
            self.entity_list.extend(EntityFactory.get_entity(self.name + "Bg"))
            self.timer = TimerController(self.name)

        # Componentes do jogo
        self.entity_manager = EntityManager(self.entity_list, self.window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(self.window)
        self.timer = TimerController(self.name)
        self.entity_manager.enable_ambient_particles = SettingsManager.get("visual_effects")
        self.entity_manager.enable_magic_fog = SettingsManager.get("visual_effects")

        if "COMPETITIVE" in game_mode:
            self.game_mode_str = "Competitivo"
        elif "COOPERATIVE" in game_mode:
            self.game_mode_str = "Cooperativo"
        else:
            self.game_mode_str = "Solo"

        if is_arcade:
            self.arcade_mode = True
            self.timer = ArcadeTimerController()
        else:
            self.arcade_mode = False
            self.timer = TimerController(self.name)

        if self.name == "Level1":
            self.sunlight = AssetManager.get_image("LightOverlay_Level1.png")
        elif self.name == "Level2":
            self.sunlight = AssetManager.get_image("LightOverlay_Level2.png")
        elif self.name == "Level3":
            self.sunlight = AssetManager.get_image("LightOverlay_Level2.png")


    def run(self, player_score: list[int]):

        if self.is_arcade:
            self.audio.play_music("arcade")
        else:
            level_name = self.name.lower()
            if level_name in ["level1", "level2", "level3"]:
                self.audio.play_music(level_name)

        clock = pygame.time.Clock()
        self.entity_manager.enable_ambient_particles = True
        self.entity_manager.enable_magic_fog = True

        for ent in self.entity_list:
            if ent.name.startswith("LightOverlay"):
                raw = AssetManager.get_image(f"{ent.name}.png")
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
