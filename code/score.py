import sys
from datetime import datetime

import pygame
from pygame import Surface, Rect, event, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from code.const import COLOR_PINK, SCORE_POS, MENU_OPTION, COLOR_WHITE
from code.dbproxy import DBProxy


class Score:

    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load("./asset/ScoreBg.png")
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save(self,game_mode:str , player_score:list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBScore')
        name = ''
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, "GATINHOS WIN!", COLOR_PINK, SCORE_POS["Title"])
            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = "Player 1 enter your name"
            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = "enter team name"
            if game_mode == MENU_OPTION[2]:
                if player_score[0] > player_score[1]:
                    score = player_score[0]
                    text = "Player 1 enter your name"
                else:
                    score = player_score[1]
                    text = "Player 2 enter your name"
            self.score_text(48, text, COLOR_PINK, SCORE_POS["EnterName"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN and len(name) == 3:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()} )
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 3:
                            name += event.unicode
            self.score_text(48, name, COLOR_WHITE, SCORE_POS["Name"])

            pygame.display.flip()
            pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, "TOP 10 SCORE", COLOR_PINK, SCORE_POS["Title"])
        self.score_text(20, "NAME     SCORE          DATE", COLOR_WHITE, SCORE_POS["Label"])
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_, name, score, date = player_score
            self.score_text(20, f"{name}    {score :05d}   {date}", COLOR_WHITE,
                                                    SCORE_POS[list_score.index(player_score)])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()


    def score_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H: %M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} {current_date}"

