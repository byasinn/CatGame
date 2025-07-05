# arcade.py - Lógica da fase Arcade integrada (com dificuldade gradual + score funcional)

import random
import pygame
from datetime import datetime
from code.system.entity import Entity
from code.system.managers.entitymanager import EntityManager
from code.system.controllers.eventcontroller import EventController
from code.core.hud import HUDRenderer
from code.factory.entityFactory import EntityFactory
from code.system.managers.assetmanager import AssetManager
from code.system.dbproxy import DBProxy
from code.core.gameover import GameOver

class Arcade:
    def __init__(self, window, game_mode, player_score, audio):
        self.window = window
        self.game_mode = game_mode
        self.audio = audio
        self.player_score = player_score

        self.player = EntityFactory.get_entity("Player1", window=window)
        self.player.score = player_score[0]
        self.entity_list: list[Entity] = [self.player]

        if game_mode.lower() in ["cooperative", "competitive"]:
            self.player2 = EntityFactory.get_entity("Player2", window=window)
            self.player2.score = player_score[1]
            self.entity_list.append(self.player2)
        else:
            self.player2 = None

        self.entity_list.extend(EntityFactory.get_entity("Level1_2Bg"))

        self.entity_manager = EntityManager(self.entity_list, window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(window)
        self.sunlight = AssetManager.get_image("LightOverlay_Level1_2.png")

        self.spawn_interval = 1200
        self.last_spawn_time = 0
        self.difficulty_timer = 0
        self.difficulty_level = 1  # Começa no nível 1

        for p in self.entity_list:
            p.entity_manager = self.entity_manager

    def run(self, player_score):
        if self.audio:
            self.audio.play_music("arcade")

        clock = pygame.time.Clock()
        self.last_spawn_time = pygame.time.get_ticks()

        while True:
            dt = clock.tick(60)
            now = pygame.time.get_ticks()
            self.difficulty_timer += dt
            self.window.fill((0, 0, 0))

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

            self.event_controller.handle(event_list)
            self.entity_manager.update_entities()
            self.entity_manager.handle_collisions()
            self.entity_manager.draw_backgrounds()
            self.entity_manager.draw_entities()
            self.hud.draw_arcade_score([self.player] if not self.player2 else [self.player, self.player2])
            self.entity_manager.draw_particles()
            self.entity_manager.update_visual_effects()

            scores = [self.player.score, self.player2.score if self.player2 else 0]
            self.hud.draw_hud(
                players=[self.player] if not self.player2 else [self.player, self.player2],
                level_name="Arcade",
                timeout=0,
                boss_summoned=False,
                fps=clock.get_fps(),
                entity_count=len(self.entity_manager.get_entities())
            )
            self.hud.draw_score(self.game_mode, scores, pygame.time.get_ticks())

            if self.difficulty_timer >= 20000:
                self.difficulty_timer = 0
                self.difficulty_level = min(self.difficulty_level + 1, 10)
                if self.spawn_interval > 400:
                    self.spawn_interval -= 50

            if now - self.last_spawn_time >= self.spawn_interval:
                enemy_pool = []
                if self.difficulty_level >= 1:
                    enemy_pool += ["Enemy1"]
                if self.difficulty_level >= 2:
                    enemy_pool += ["Enemy2"]
                if self.difficulty_level >= 4:
                    enemy_pool += ["Enemy3"]

                enemies_to_spawn = min(1 + self.difficulty_level // 3, 4)

                for _ in range(enemies_to_spawn):
                    enemy_type = random.choice(enemy_pool)
                    enemy = EntityFactory.get_entity(enemy_type, window=self.window)
                    enemy.entity_manager = self.entity_manager
                    self.entity_manager.add_entity(enemy)

                self.last_spawn_time = now

            if not self.entity_manager.is_player_alive():
                # ✅ Salva score no banco de dados (só no modo arcade solo)
                if self.game_mode.lower() == "solo":
                    db = DBProxy("DBScore")
                    db.insert_score("Player1", self.player.score, datetime.now())
                    db.close()

                return GameOver(self.window).show()

            pygame.display.flip()