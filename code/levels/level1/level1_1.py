import sys
import pygame
from pygame import Surface
from code.settings.settingsmanager import SettingsManager
from code.system.managers.assetmanager import AssetManager
from code.system.entity import Entity
from code.factory.entityFactory import EntityFactory
from code.core.hud import HUDRenderer
from code.system.controllers.eventcontroller import EventController
from code.system.managers.entitymanager import EntityManager

# Importa os novos módulos separados
from code.levels.level1.tutorialmanager import TutorialManager
from code.levels.level1.cutscenes1 import CutsceneManager, run_scene


class Level1_0:
    def __init__(self, window: Surface, game_mode: str, player_score: list[int], audio=None):
        self.window = window
        self.name = "Level1"
        self.game_mode = game_mode
        self.audio = audio
        self.entity_list: list[Entity] = []

        # Cria jogador
        self.player = EntityFactory.get_entity('Player1', window=window)
        self.player.score = player_score[0]
        self.entity_list.append(self.player)

        if "COOPERATIVE" in game_mode.upper() or "2P" in game_mode.upper():
            self.player2 = EntityFactory.get_entity('Player2', window=window)
            self.player2.score = player_score[1]
            self.entity_list.append(self.player2)

        # Carrega fundo
        self.entity_list.extend(EntityFactory.get_entity("Level1Bg"))

        # Setup geral
        self.entity_manager = EntityManager(self.entity_list, self.window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(self.window)
        self.sunlight = AssetManager.get_image("LightOverlay_Level1_1Bg.png")

        self.effects_enabled = SettingsManager.get("visual_effects")
        self.entity_manager.enable_ambient_particles = self.effects_enabled
        self.entity_manager.enable_magic_fog = self.effects_enabled

        # Atribui managers aos players
        self.player.entity_manager = self.entity_manager
        if hasattr(self, "player2"):
            self.player2.entity_manager = self.entity_manager

        # Managers externos (tutorial e cutscene)
        self.tutorial_manager = TutorialManager(self.entity_manager, self.window, self.player)
        self.cutscene_manager = CutsceneManager(self.window, self.player)

        self.phase = "tutorial"  # tutorial → cutscene → gameplay
        self.phase_timer_started = False
        self.start_time = None
        self.last_spawn_time = 0
        self.spawn_interval = 2000  # 2 segundos

        self.max_duration = 1000


    def run(self, player_score: list[int]):
        if self.audio:
            self.audio.play_music("level1")
        run_scene(self.window, "scenes1")

        clock = pygame.time.Clock()
        self.phase = "tutorial"
        self.phase_timer_started = False
        self.start_time = None
        self.last_spawn_time = 0
        self.spawn_interval = 2000  # ms

        while True:
            dt = clock.tick(60)
            now = pygame.time.get_ticks()
            self.window.fill((0, 0, 0))
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.event_controller.handle(event_list)

            self.entity_manager.update_entities()
            self.entity_manager.handle_collisions()
            self.entity_manager.draw_backgrounds()
            self.entity_manager.draw_entities()
            self.entity_manager.draw_particles()
            self.entity_manager.update_visual_effects()

            # FASE 1: Tutorial
            if self.phase == "tutorial":
                self.tutorial_manager.update()
                if self.tutorial_manager.done:
                    self.phase = "cutscene"



            # FASE 2: Cutscene
            elif self.phase == "cutscene":
                self.cutscene_manager.update(event_list)
                if self.cutscene_manager.done:
                    self.phase = "gameplay"
                    self.start_time = now
                    self.last_spawn_time = now

            # FASE 3: Gameplay real
            elif self.phase == "gameplay":
                elapsed_ms = now - self.start_time

                self.hud.draw_hud(
                    players=[self.player],
                    level_name=self.name,
                    timeout=elapsed_ms,
                    boss_summoned=False,
                    fps=clock.get_fps(),
                    entity_count=len(self.entity_manager.get_entities())
                )

                if now - self.last_spawn_time >= self.spawn_interval:
                    enemy = EntityFactory.get_entity("Enemy1", window=self.window)
                    self.entity_manager.add_entity(enemy)
                    self.last_spawn_time = now

                # ⏭️ Transição para o próximo nível (level1_2)
                if elapsed_ms >= self.max_duration:
                    return True

            if not self.entity_manager.is_player_alive():
                return False

            pygame.display.flip()

