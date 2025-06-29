#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from code.settings.display import apply_resolution
from code.settings.settingsmenu import SettingsMenu
from code.assetmanager import AssetManager
from code.level import Level
from code.menu import Menu
from code.score import Score
from code.gameover import GameOver
from code.const import MENU_OPTION
from code.settings.settingsmenu import SettingsMenu
from code.audiocontroller import AudioController
from code.lang import t

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
                is_arcade = game_type == "ARCADE"

                if game_type == "CAMPANHA":
                    mode = menu.select_campaign_mode()
                    if mode == "BACK":
                        continue
                    menu_return = "NEW GAME 1P" if mode == "SOLO" else "NEW GAME 2P - COOPERATIVE"
                else:
                    mode = menu.select_arcade_mode()
                    if mode == "BACK":
                        continue
                    menu_return = "NEW GAME 1P" if mode == "SOLO" else "NEW GAME 2P - COMPETITIVE"

                player_score = [0, 0]

                if is_arcade:
                    self.fade(fade_in=True)
                    level = Level(self.window, 'LevelArcade', menu_return, player_score, is_arcade=True, audio=self.audio)
                    level_return = level.run(player_score)
                    self.fade(fade_in=False)

                    GameOver(self.window).show()
                    continue

                # 🔐 A PARTIR DAQUI: CAMPANHA
                self.show_intro_dialogue(menu_return, phase=1)
                self.fade(fade_in=True)
                level = Level(self.window, 'Level1', menu_return, player_score, audio=self.audio)
                level_return = level.run(player_score)
                self.fade(fade_in=False)
                if not level_return:
                    GameOver(self.window).show()
                    continue

                self.show_intro_dialogue(menu_return, phase=2)
                self.fade(fade_in=True)
                level = Level(self.window, 'Level2', menu_return, player_score, audio=self.audio)
                level_return = level.run(player_score)
                self.fade(fade_in=False)
                if not level_return:
                    GameOver(self.window).show()
                    continue

                self.show_intro_dialogue(menu_return, phase=3)
                self.fade(fade_in=True)
                level = Level(self.window, 'Level3', menu_return, player_score, audio=self.audio)
                self.fade(fade_in=False)
                level_return = level.run(player_score)
                if not level_return:
                    GameOver(self.window).show()
                    continue

                score.save(menu_return, player_score)

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

        # Gatinhos
        leon = AssetManager.get_image(f"LeonMenu{'' if phase == 1 else phase}.png")
        mora = AssetManager.get_image(f"MoraMenu{'' if phase == 1 else phase}.png")
        leon_rect = leon.get_rect(bottomleft=(50, self.window.get_height() - 30))
        mora_rect = mora.get_rect(bottomright=(self.window.get_width() - 50, self.window.get_height() - 30))

        # Fonte
        font = AssetManager.get_font("VT323-Regular.ttf", 22)

        # Diálogos
        dialogues = [t(f"cutscene{phase}_{i + 1}") for i in range(3)]

        current = 0

        while True:
            self.window.fill((0, 0, 0))
            self.window.blit(leon, leon_rect)
            self.window.blit(mora, mora_rect)

            # Renderizar texto atual
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
                        return  # termina o diálogo e vai pro jogo

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