#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from code.levels.level1.level1_1 import Level1_0
from code.settings.display import apply_resolution
from code.system.assetmanager import AssetManager
from code.levels.level import Level  # <- Esse agora é o loader com PHASE_MAP
from code.core.menu import Menu
from code.core.score import Score
from code.core.gameover import GameOver
from code.settings.settingsmenu import SettingsMenu
from code.system.audiocontroller import AudioController
from code.settings.lang import t
from code.levels.level1.cutscenes1 import run_scene
from code.system.particle import draw_grain_overlay


class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.window = apply_resolution()
        self.audio = AudioController()

    def run(self):
        self.show_intro_screen()
        self.audio.play_music("menu")

        while True:
            score = Score(self.window)
            menu = Menu(self.window, self.audio)

            menu_return = menu.run()

            if menu_return == "NEW GAME":
                game_type = menu.select_mode()
                if game_type == "BACK":
                    continue

                if game_type.lower() == "campaign":
                    is_arcade = False
                    mode = menu.select_campaign_mode()
                elif game_type.lower() == "arcade":
                    is_arcade = True
                    mode = menu.select_arcade_mode()
                else:
                    continue

                player_score = [0, 0]

                self.fade(fade_in=True)
                level = Level(self.window, 'Level1', mode, player_score, is_arcade=is_arcade, audio=self.audio)
                level_return = level.run(player_score)
                self.fade(fade_in=False)

                if not level_return:
                    GameOver(self.window).show()
                    continue

                self.fade(fade_in=True)
                level = Level(self.window, 'Level1', menu_return, player_score, audio=self.audio)
                level_return = level.run(player_score)
                self.fade(fade_in=False)

                if not level_return:
                    GameOver(self.window).show()
                    continue

            elif menu_return == "SCORE":
                score.show()

            elif menu_return == "SETTINGS":
                SettingsMenu(self.window, self.audio).run()

            elif menu_return == "EXIT":
                pygame.quit()
                quit()

    def show_intro_screen(self):
        intro_img = AssetManager.get_image("IntroScreen.png")
        intro_img = pygame.transform.scale(intro_img, (self.window.get_width(), self.window.get_height()))
        draw_grain_overlay(self.window)

        if not pygame.mixer_music.get_busy():
            self.audio.play_music("intro")

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        intro_duration = 5000
        skipped = False

        while not skipped and pygame.time.get_ticks() - start_time < intro_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        skipped = True

            self.window.fill((0, 0, 0))
            alpha = min(255, int((pygame.time.get_ticks() - start_time) / 20))
            img_copy = intro_img.copy()
            img_copy.set_alpha(alpha)
            self.window.blit(img_copy, (0, 0))
            pygame.display.flip()
            clock.tick(60)

    def show_intro_dialogue(self, game_mode, phase=1):
        leon = AssetManager.get_image(f"LeonMenu{'' if phase == 1 else phase}.png")
        mora = AssetManager.get_image(f"MoraMenu{'' if phase == 1 else phase}.png")
        leon_rect = leon.get_rect(bottomleft=(50, self.window.get_height() - 30))
        mora_rect = mora.get_rect(bottomright=(self.window.get_width() - 50, self.window.get_height() - 30))

        font = AssetManager.get_font("VT323-Regular.ttf", 22)
        dialogues = [t(f"cutscene{phase}_{i + 1}") for i in range(3)]

        current = 0

        while True:
            self.window.fill((0, 0, 0))
            self.window.blit(leon, leon_rect)
            self.window.blit(mora, mora_rect)

            text = font.render(dialogues[current], True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
            self.window.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if current < len(dialogues) - 1:
                        current += 1
                    else:
                        return

    def fade(self, fade_in=True, speed=10):
        fade_surface = pygame.Surface(self.window.get_size()).convert()
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()

        alpha_range = range(255, -1, -speed) if fade_in else range(0, 256, speed)

        for alpha in alpha_range:
            fade_surface.set_alpha(alpha)
            self.window.blit(fade_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)
