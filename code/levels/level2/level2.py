#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from pygame import Surface

from code.settings.settingsmanager import SettingsManager
from code.system.managers.assetmanager import AssetManager
from code.system.config import MENU_OPTION
from code.system.managers.entitymanager import EntityManager
from code.system.entity import Entity
from code.factory.entityFactory import EntityFactory
from code.core.hud import HUDRenderer
from code.system.controllers.timercontroller import TimerController
from code.system.controllers.eventcontroller import EventController
from code.settings.lang import t


class Level2:
    def __init__(self, window: Surface, game_mode: str, player_score: list[int], audio=None):
        self.window = window
        self.name = "Level2"
        self.game_mode = game_mode
        self.audio = audio
        self.entity_list: list[Entity] = []

        # Criar jogadores
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        # Fundo da fase
        self.entity_list.extend(EntityFactory.get_entity("Level2Bg"))

        # Timer da campanha
        self.timer = TimerController(self.name)

        # Componentes do jogo
        self.entity_manager = EntityManager(self.entity_list, self.window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(self.window)
        self.entity_manager.enable_ambient_particles = SettingsManager.get("visual_effects")
        self.entity_manager.enable_magic_fog = SettingsManager.get("visual_effects")

        # Configuração de game mode no HUD
        if "COMPETITIVE" in game_mode:
            self.game_mode_str = "Competitivo"
        elif "COOPERATIVE" in game_mode:
            self.game_mode_str = "Cooperativo"
        else:
            self.game_mode_str = "Solo"

        # Overlay de luz
        self.sunlight = AssetManager.get_image("LightOverlay_Level2.png")

    def run(self, player_score: list[int]):
        if self.audio:
            self.audio.play_music("level2")

        clock = pygame.time.Clock()

        for ent in self.entity_list:
            if ent.name.startswith("LightOverlay"):
                raw = AssetManager.get_image(f"{ent.name}.png")
                w, h = self.window.get_size()
                ent.surf = pygame.transform.scale(raw, (w, h))

        while True:
            clock.tick(60)
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_action = self.draw_pause_menu()

                    if pause_action == "resume":
                        continue
                    elif pause_action == "settings":
                        from code.settings.settingsmenu import SettingsMenu
                        SettingsMenu(self.window, self.audio).run()
                    elif pause_action == "main_menu":
                        return None
                    elif pause_action == "quit":
                        pygame.quit()
                        exit()

            self.event_controller.handle(event_list)
            event_result = self.timer.update(event_list, self.entity_manager.get_entities(), EntityFactory)

            if event_result == "complete":
                for p in self.entity_manager.get_players():
                    if p.name == "Player1":
                        player_score[0] = p.score
                    elif p.name == "Player2":
                        player_score[1] = p.score
                return True

            self.entity_manager.draw_backgrounds()
            self.entity_manager.draw_entities()
            self.entity_manager.draw_particles()
            self.entity_manager.update_entities()
            self.entity_manager.update_visual_effects()
            self.entity_manager.handle_collisions()

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

            pygame.display.flip()

    def draw_pause_menu(self):
        options = ["resume", "settings", "main_menu", "quit"]
        selected = 0
        clock = pygame.time.Clock()

        while True:
            self.window.fill((0, 0, 0, 180))
            overlay = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.window.blit(overlay, (0, 0))

            font = pygame.font.Font("./asset/PressStart2P-Regular.ttf", 24)

            for i, key in enumerate(options):
                label = t(key)
                color = (255, 255, 255) if i == selected else (180, 180, 180)
                text = font.render(label, True, color)
                rect = text.get_rect(center=(self.window.get_width() // 2, 200 + i * 40))
                self.window.blit(text, rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selected]
                    elif event.key == pygame.K_ESCAPE:
                        return "resume"

            clock.tick(30)
