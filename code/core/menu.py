#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys
import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.core.loadgame import LoadGame
from code.devtools import handle_dev_keys
from code.factory.backgroundfactory import BackgroundFactory
from code.settings.lang import t
from code.system.managers.assetmanager import AssetManager
from code.system.config import MENU_OPTION, COLOR_WHITE, COLOR_YELLOW, COLOR_PINK
from code.system.keys import MENU_KEYS
from code.system.particle import draw_grain_overlay
from code.system.managers.gamemanager import GameManager
from code.core.score import Score
from code.settings.settingsmenu import SettingsMenu
from code.core.gameover import GameOver

class Menu:
    def __init__(self, window, audio_controller):
        self.window = window
        self.audio = audio_controller
        self.cat_left = AssetManager.get_image("LeonMenu.png")
        self.cat_right = AssetManager.get_image("MoraMenu.png")
        self.bg_list = []
        self.manager = GameManager(self.window, self.audio)

    def run_loop(self):
        while True:
            selected = self.run()

            if selected == "NEW GAME":
                mode_type = self.select_mode()
                if mode_type == "BACK":
                    continue

                if mode_type.lower() == "campaign":
                    mode = self.select_campaign_mode()
                    if mode != "BACK":
                        result = self.manager.start_campaign(mode)
                        if not result:
                            GameOver(self.window).show()

                elif mode_type.lower() == "arcade":
                    mode = self.select_arcade_mode()
                    if mode != "BACK":
                        result = self.manager.start_arcade(mode)
                        if not result:
                            GameOver(self.window).show()


            elif selected == "LOAD GAME":
                from code.core.loadgame import LoadGame
                result = LoadGame.run_load_game(self.window, self.audio)



            elif selected == "SCORE":
                Score(self.window).show()

            elif selected == "SETTINGS":
                SettingsMenu(self.window, self.audio).run()

            elif selected == "EXIT":
                pygame.quit()
                quit()

    def run(self):
        menu_option = 0
        self.bg_list = BackgroundFactory.create("Menu")
        if self.audio.current_music != "menu":
            self.audio.play_music("menu")

        while True:
            for bg in self.bg_list:
                bg.move()
                self.window.blit(bg.surf, bg.rect)

            width, height = self.window.get_size()
            self.menu_text(50, t("title_main1"), COLOR_PINK, (width // 2, int(height * 0.08)), is_title=True)
            self.menu_text(50, t("title_main2"), COLOR_PINK, (width // 2, int(height * 0.15)), is_title=True)

            options = ["NEW GAME", "LOAD GAME", "SCORE", "SETTINGS", "EXIT"]
            option_start_y = int(height * 0.35)
            option_spacing = int(height * 0.07)

            for i in range(len(options)):
                color = COLOR_YELLOW if i == menu_option else COLOR_WHITE
                y_pos = option_start_y + i * option_spacing
                self.menu_text(20, t(options[i].lower()), color, (width // 2, y_pos))

            draw_grain_overlay(self.window)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in MENU_KEYS["down"]:
                        menu_option = (menu_option + 1) % len(options)
                        self.audio.play_sound("menu_move")
                    if event.key in MENU_KEYS["up"]:
                        menu_option = (menu_option - 1) % len(options)
                        self.audio.play_sound("menu_move")
                    if event.key in MENU_KEYS["select"]:
                        self.audio.play_sound("menu_select")
                        return options[menu_option]
                if handle_dev_keys(event, self.window, self.audio):
                    return

    def select_mode(self):
        return self.run_options(["campaign", "arcade"], "mode_select_title")

    def select_campaign_mode(self):
        return self.run_options(["solo", "cooperative"], "campaign")

    def select_arcade_mode(self):
        return self.run_options(["solo", "competitive"], "arcade")

    def run_options(self, options, title):
        selected = 0
        self.bg_list = BackgroundFactory.create("Menu")
        while True:
            for bg in self.bg_list:
                bg.move()
                self.window.blit(bg.surf, bg.rect)

            width, height = self.window.get_size()
            self.menu_text(40, t(title), COLOR_PINK, (width // 2, int(height * 0.1)), True)

            option_start_y = int(height * 0.3)
            option_spacing = int(height * 0.08)
            options_translated = [t(opt.lower()) for opt in options]

            slots = LoadGame.get_all_slots()

            for i, label in enumerate(options_translated):
                color = COLOR_YELLOW if i == selected else COLOR_WHITE
                y_pos = option_start_y + i * option_spacing
                self.menu_text(24, label, color, (width // 2, y_pos))

            draw_grain_overlay(self.window)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in MENU_KEYS["up"]:
                        selected = (selected - 1) % len(options)
                        self.audio.play_sound("menu_move")
                    elif event.key in MENU_KEYS["down"]:
                        selected = (selected + 1) % len(options)
                        self.audio.play_sound("menu_move")
                    elif event.key in MENU_KEYS["select"]:
                        self.audio.play_sound("menu_select")
                        return options[selected]
                    elif event.key in MENU_KEYS["back"]:
                        return "BACK"

    def draw_cats(self):
        width, height = self.window.get_size()
        center_y = int(height * 0.15)
        offset_x = int(width * 0.18)

        cat_left_center = (width // 2 - offset_x, center_y)
        cat_right_center = (width // 2 + offset_x, center_y)

        offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        angle = math.sin(pygame.time.get_ticks() * 0.002) * 5

        rotated_left = pygame.transform.rotate(self.cat_left, angle)
        left_rect = rotated_left.get_rect(center=(cat_left_center[0], cat_left_center[1] + offset))
        self.window.blit(rotated_left, left_rect)

        rotated_right = pygame.transform.flip(self.cat_right, True, False)
        rotated_right = pygame.transform.rotate(rotated_right, -angle)
        right_rect = rotated_right.get_rect(center=(cat_right_center[0], cat_right_center[1] + offset))
        self.window.blit(rotated_right, right_rect)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple, is_title: bool = False):
        font_name = "PressStart2P-Regular.ttf" if is_title else "VT323-Regular.ttf"
        text_font: Font = AssetManager.get_font(font_name, text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
        self.draw_cats()