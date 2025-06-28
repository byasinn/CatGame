#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code import settings
from code.level import Level
from code.menu import Menu
from code.score import Score
from code.gameover import GameOver
from code.const import MENU_OPTION
from code.settingsmenu import SettingsMenu

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.window = settings.apply_resolution()

    def run(self):
        self.show_intro_screen()

        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                self.show_intro_dialogue(menu_return, phase=1)
                player_score = [0, 0]

                level = Level(self.window, 'Level1', menu_return, player_score)
                level_return = level.run(player_score)
                if not level_return:
                    GameOver(self.window).show()
                    continue

                self.show_intro_dialogue(menu_return, phase=2)
                level = Level(self.window, 'Level2', menu_return, player_score)
                level_return = level.run(player_score)
                if not level_return:
                    GameOver(self.window).show()
                    continue

                self.show_intro_dialogue(menu_return, phase=3)
                level = Level(self.window, 'Level3', menu_return, player_score)
                level_return = level.run(player_score)
                if not level_return:
                    GameOver(self.window).show()
                    continue

                score.save(menu_return, player_score)

            elif menu_return == MENU_OPTION[3]:
                score.show()


            elif menu_return == MENU_OPTION[4]:  # SETTINGS
                from code.settingsmenu import SettingsMenu
                SettingsMenu(self.window).run()

            elif menu_return == MENU_OPTION[5]:
                pygame.quit()
                quit()
            else:
                pass

    def show_intro_screen(self):
        intro_img = pygame.image.load("./asset/IntroScreen.png").convert_alpha()
        intro_img = pygame.transform.scale(intro_img, (self.window.get_width(), self.window.get_height()))

        pygame.mixer_music.load("./asset/intro.mp3")
        pygame.mixer_music.play()

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 5000:  # 5 segundos
            self.window.fill((0, 0, 0))
            alpha = min(255, int((pygame.time.get_ticks() - start_time) / 20))
            img_copy = intro_img.copy()
            img_copy.set_alpha(alpha)
            self.window.blit(img_copy, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(60)

    def show_intro_dialogue(self, game_mode, phase=1):

        # Gatinhos
        leon = pygame.image.load(f"./asset/LeonMenu{'' if phase == 1 else phase}.png").convert_alpha()
        mora = pygame.image.load(f"./asset/MoraMenu{'' if phase == 1 else phase}.png").convert_alpha()
        leon_rect = leon.get_rect(bottomleft=(50, self.window.get_height() - 30))
        mora_rect = mora.get_rect(bottomright=(self.window.get_width() - 50, self.window.get_height() - 30))

        # Fonte
        font = pygame.font.Font("./asset/VT323-Regular.ttf", 22)

        # Diálogos
        if phase == 1:
            dialogues = [
                "Leon: Miau, parece que vamos ter um dia cheio!",
                "Mora: Cuidado com os inimigos, viu? Eu confio em você ♥",
                "Pressione ENTER para começar!"
            ]
        elif phase == 2:
            dialogues = [
                "Mora: Ufa, essa foi difícil!",
                "Leon: A próxima fase vai ser ainda mais intensa, miaaau!",
                "Preparadx? Aperte ENTER!"
            ]
        elif phase == 3:
            dialogues = [
                "Leon: É agora, o último desafio!",
                "Mora: Mostre que você é uma verdadeira lenda felina!",
                "Aperte ENTER e brilhe!"
            ]

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


