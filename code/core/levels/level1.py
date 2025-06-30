import sys
import pygame
import math
from pygame import Surface
from code.settings.settingsmanager import SettingsManager
from code.system.assetmanager import AssetManager
from code.system.config import MENU_OPTION
from code.system.entitymanager import EntityManager
from code.system.entity import Entity
from code.factory.entityFactory import EntityFactory
from code.core.hud import HUDRenderer
from code.system.eventcontroller import EventController
from code.settings.lang import t

class Level1_0:
    def __init__(self, window: Surface, game_mode: str, player_score: list[int], audio=None):
        self.window = window
        self.name = "Level1"
        self.game_mode = game_mode
        self.audio = audio
        self.entity_list: list[Entity] = []

        self.tutorial_step = 0
        self.tutorial_done = False
        self.enemy_spawned = False
        self.dialogue_phase = 0
        self.dialogue_done = False

        # Criar jogador
        self.player = EntityFactory.get_entity('Player1', window=window)
        self.player.score = player_score[0]
        self.entity_list.append(self.player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.player2 = EntityFactory.get_entity('Player2', window=window)
            self.player2.score = player_score[1]
            self.entity_list.append(self.player2)

        self.entity_list.extend(EntityFactory.get_entity("Level1Bg"))

        self.entity_manager = EntityManager(self.entity_list, self.window)
        self.event_controller = EventController(self.entity_manager, EntityFactory)
        self.hud = HUDRenderer(self.window)

        self.sunlight = AssetManager.get_image("LightOverlay_Level1.png")

        self.effects_enabled = SettingsManager.get("visual_effects")
        self.entity_manager.enable_ambient_particles = self.effects_enabled
        self.entity_manager.enable_magic_fog = self.effects_enabled

        self.player.entity_manager = self.entity_manager

        # NPC Dialog
        self.dialogue_list = [
            ("npc", "Que bom que você já chegou, eles estão por toda parte!"),
            ("player", "Onde? Quem?"),
            ("npc", "Fique atento, não confie em ninguém!"),
        ]
        self.npc_img = AssetManager.get_image("NpcSprite.png")
        self.npc_pos_x = window.get_width() + 100
        self.npc_target_x = window.get_width() // 2 + 80

    def run(self, player_score: list[int]):
        if self.audio:
            self.audio.play_music("level1")

        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(60)
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

            if not self.tutorial_done:
                self.update_tutorial()
            else:
                self.update_dialogue(event_list)

            pygame.display.flip()

            if self.dialogue_done:
                import time
                time.sleep(1)
                return True

    def update_tutorial(self):
        keys = pygame.key.get_pressed()
        player = self.player

        if self.tutorial_step == 0:
            self.draw_text("Mova-se com as setas ou WASD")
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
                self.tutorial_step += 1

        elif self.tutorial_step == 1:
            self.draw_text("Atire com Ctrl")
            if player.shot_fired:
                self.tutorial_step += 1

        elif self.tutorial_step == 2:
            self.draw_text("Derrote o inimigo!")
            if not self.enemy_spawned:
                enemy = EntityFactory.get_entity("EnemyTest", window=self.window)
                enemy.hp = 1
                enemy.frozen = False
                self.entity_manager.add_entity(enemy)
                self.enemy_spawned = True
            if not any(e.name == "EnemyTest" for e in self.entity_manager.get_entities()):
                self.tutorial_step += 1

        elif self.tutorial_step == 3:
            self.draw_text("Parabéns! Prepare-se...", darken=False)
            self.tutorial_done = True

    def update_dialogue(self, event_list):
        # Animação NPC voando da direita
        if self.npc_pos_x > self.npc_target_x:
            self.npc_pos_x -= 6

        npc_y = self.window.get_height() // 2 + math.sin(pygame.time.get_ticks() * 0.005) * 8
        npc_rect = self.npc_img.get_rect(center=(self.npc_pos_x, npc_y))
        self.window.blit(self.npc_img, npc_rect)

        if self.npc_pos_x <= self.npc_target_x:
            if self.dialogue_phase < len(self.dialogue_list):
                speaker, message = self.dialogue_list[self.dialogue_phase]
                font = pygame.font.Font("./asset/PressStart2P-Regular.ttf", 14)
                wrapped_lines = self.render_wrapped_text(message, font, self.window.get_width() // 2.5)

                if speaker == "npc":
                    base_pos = (npc_rect.centerx, npc_rect.top - 30)
                else:
                    base_pos = (self.player.rect.centerx, self.player.rect.top - 30)

                for i, line in enumerate(wrapped_lines):
                    rect = line.get_rect(center=(base_pos[0], base_pos[1] + i * 18))
                    self.window.blit(line, rect)

                for event in event_list:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.dialogue_phase += 1
            else:
                self.dialogue_done = True

    def draw_text(self, message: str, darken=False, blink=False):
        self.hud.draw_tutorial_message(self.window, message, darken=darken, blink=blink)

    def render_wrapped_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = current + word + " "
            if font.size(test)[0] < max_width:
                current = test
            else:
                lines.append(font.render(current.strip(), True, (255, 255, 255)))
                current = word + " "
        if current:
            lines.append(font.render(current.strip(), True, (255, 255, 255)))
        return lines

class Level1:
    pass