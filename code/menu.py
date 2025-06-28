#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.const import WIN_WIDTH, MENU_OPTION, COLOR_WHITE, COLOR_YELLOW, COLOR_PINK


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./asset/MenuBg.png")
        self.rect = self.surf.get_rect(left=0, top=0)
        self.cat_left = pygame.image.load("./asset/LeonMenu.png").convert_alpha()
        self.cat_right = pygame.image.load("./asset/MoraMenu.png").convert_alpha()
        self.cat_left_rect = self.cat_left.get_rect(center=(WIN_WIDTH // 2 - 150, 95))
        self.cat_right_rect = self.cat_right.get_rect(center=(WIN_WIDTH // 2 + 150, 95))
        self.cat_angle = 0

    def run(self, ):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            # draw images
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Mora", COLOR_PINK, ((WIN_WIDTH / 2), 70), is_title=True)
            self.menu_text(50, "Migos", COLOR_WHITE, ((WIN_WIDTH / 2), 120), is_title=True)

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], COLOR_YELLOW, ((WIN_WIDTH / 2), 200 + 25 * i), is_title=False)
                else:
                    self.menu_text(20, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 200 + 25 * i), is_title=False)
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close window
                    quit()  # End pyGame
                if event.type == pygame.KEYDOWN: #DOWN KEY
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP: # up key
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN: # ENTER
                        return MENU_OPTION[menu_option]

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
        font_path = "./asset/PressStart2P-Regular.ttf" if is_title else "./asset/VT323-Regular.ttf"
        text_font: Font = pygame.font.Font(font_path, text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

        self.draw_cats()
