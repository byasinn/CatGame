import sys
import pygame
from pygame import Surface
from code.system.assetmanager import AssetManager
from code.system.entitymanager import EntityManager
from code.factory.entityFactory import EntityFactory
from code.core.hud import HUDRenderer
from code.system.eventcontroller import EventController
from code.system.config import MENU_OPTION
from code.settings.settingsmanager import SettingsManager
from code.system.entity import Entity

class Level1_2:
    def __init__(self, window: Surface, game_mode: str, player_score: list[int], audio=None):
        self.window = window
        self.game_mode = game_mode
        self.audio = audio
        self.name = "Level1_2"
        self.entity_list: list[Entity] = []

        # Jogador principal
        self.player = EntityFactory.get_entity('Player1', window=window)
        self.player.score = player_score[0]
        self.entity_list.append(self.player)


        # Cooperativo (se aplicável)
        if game_mode.lower() in ["cooperative", "competitive"]:
            self.player2 = EntityFactory.get_entity('Player2', window=window)
            self.player2.score = player_score[1]
            self.entity_list.append(self.player2)

        # Fundo
        self.entity_list.extend(EntityFactory.get_entity("Level1_2Bg"))
        self.entity_list.extend(EntityFactory.get_entity("Foreground1_2Bg"))

        # Componentes principais
        self.entity_manager = EntityManager(self.entity_list, self.window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(self.window)
        self.sunlight = AssetManager.get_image("LightOverlay_Level1.png")

        # Efeitos visuais
        effects = SettingsManager.get("visual_effects")
        self.entity_manager.enable_ambient_particles = effects
        self.entity_manager.enable_magic_fog = effects
        self.player.entity_manager = self.entity_manager
        if hasattr(self, "player2"):
            self.player2.entity_manager = self.entity_manager

        # Timer e spawn
        self.max_duration = 30000  # 30 segundos
        self.start_time = None
        self.last_spawn_time = 0
        self.spawn_interval = 1500  # 1.5s
        self.enemy_toggle = True  # alternador de inimigos

    def run(self, player_score: list[int]):
        if self.audio:
            self.audio.play_music("level1")

        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = self.start_time

        while True:
            dt = clock.tick(60)
            now = pygame.time.get_ticks()
            elapsed_ms = now - self.start_time
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

            for entity in self.entity_manager.get_entities():
                if "Foreground1_2Bg" in entity.name:
                    entity.move()
                    self.window.blit(entity.surf, entity.rect)

            self.hud.draw_hud(
                players=[self.player],
                level_name=self.name,
                timeout=elapsed_ms,
                boss_summoned=False,
                fps=clock.get_fps(),
                entity_count=len(self.entity_manager.get_entities())
            )

            # Spawn de inimigos alternando entre Enemy1 e Enemy2
            if now - self.last_spawn_time >= self.spawn_interval:
                enemy_type = "Enemy1" if self.enemy_toggle else "Enemy2"
                enemy = EntityFactory.get_entity(enemy_type, window=self.window)
                self.entity_manager.add_entity(enemy)
                self.enemy_toggle = not self.enemy_toggle
                self.last_spawn_time = now

            # Terminar fase após o tempo
            if elapsed_ms >= self.max_duration:
                return True

            pygame.display.flip()
