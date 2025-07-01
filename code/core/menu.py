#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys
import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.factory.backgroundfactory import BackgroundFactory
from code.settings.lang import t
from code.system.assetmanager import AssetManager
from code.system.config import MENU_OPTION, COLOR_WHITE, COLOR_YELLOW, COLOR_PINK


class Menu:
    def __init__(self, window, audio_controller):
        self.window = window
        self.audio = audio_controller
        self.cat_left = AssetManager.get_image("LeonMenu.png")
        self.cat_right = AssetManager.get_image("MoraMenu.png")
        self.cat_left_rect = self.cat_left.get_rect(center=(self.window.get_width() // 2 - 150, 95))
        self.cat_right_rect = self.cat_right.get_rect(center=(self.window.get_width() // 2 + 150, 95))
        self.cat_angle = 0
        self.bg_list = BackgroundFactory.create("Menu")

    def run(self, ):
        menu_option = 0
        if self.audio.current_music != "menu":
            self.audio.play_music("menu")

        while True:
            # draw images
            for bg in self.bg_list:
                bg.move()
                self.window.blit(bg.surf, bg.rect)

            self.menu_text(50, t("title_main1"), COLOR_PINK, ((self.window.get_width() / 2), 70), is_title=True)
            self.menu_text(50, t("title_main2"), COLOR_WHITE, ((self.window.get_width() / 2), 120), is_title=True)

            options = [t("new_game"), t("score"), t("settings"), t("exit")]
            for i in range(len(options)):
                color = COLOR_YELLOW if i == menu_option else COLOR_WHITE
                self.menu_text(20, options[i], color, ((self.window.get_width() / 2), 200 + 25 * i))
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                        self.audio.play_sound("menu_move")
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                        self.audio.play_sound("menu_move")

                    if event.key == pygame.K_RETURN:
                        self.audio.play_sound("menu_select")
                        return ["NEW GAME", "SCORE", "SETTINGS", "EXIT"][menu_option]

    def select_mode(self):
        return self.run_options(["campaign", "arcade"], "mode_select_title")

    def select_campaign_mode(self):
        return self.run_options(["solo", "cooperative"], "campaign")

    def select_arcade_mode(self):
        return self.run_options(["solo", "competitive"], "arcade")

    def run_options(self, options, title):
        selected = 0

        while True:
            for bg in self.bg_list:
                bg.move()
                self.window.blit(bg.surf, bg.rect)

            self.menu_text(40, t(title), COLOR_PINK, (self.window.get_width() // 2, 70), True)

            options_translated = [t(opt.lower()) for opt in options]
            for i, label in enumerate(options_translated):
                color = COLOR_YELLOW if i == selected else COLOR_WHITE
                self.menu_text(24, label, color, (self.window.get_width() // 2, 150 + i * 40), False)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                        self.audio.play_sound("menu_move")
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                        self.audio.play_sound("menu_move")
                    elif event.key == pygame.K_RETURN:
                        self.audio.play_sound("menu_select")
                        return options[selected]
                    elif event.key == pygame.K_ESCAPE:
                        return "BACK"

    def draw_cats(self):
        offset = math.sin(pygame.time.get_ticks() * 0.005) * 2  # animação vertical
        angle = math.sin(pygame.time.get_ticks() * 0.002) * 5   # rotação leve

        # Esquerdo
        rotated_left = pygame.transform.rotate(self.cat_left, angle)
        left_rect = rotated_left.get_rect(center=(self.cat_left_rect.centerx, self.cat_left_rect.centery + offset))
        self.window.blit(rotated_left, left_rect)

        # Direito (espelhado)
        rotated_right = pygame.transform.flip(self.cat_right, True, False)
        rotated_right = pygame.transform.rotate(rotated_right, -angle)
        right_rect = rotated_right.get_rect(center=(self.cat_right_rect.centerx, self.cat_right_rect.centery + offset))
        self.window.blit(rotated_right, right_rect)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple, is_title: bool = False):
        font_name = "PressStart2P-Regular.ttf" if is_title else "VT323-Regular.ttf"
        text_font: Font = AssetManager.get_font(font_name, text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

        self.draw_cats()
