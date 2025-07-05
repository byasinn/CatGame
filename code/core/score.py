# score.py - tela de scores com música do menu e suporte a resolução

import sys
from datetime import datetime
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.system.keys import MENU_KEYS
from code.system.managers.assetmanager import AssetManager
from code.system.controllers.audiocontroller import AudioController
from code.system.config import COLOR_PINK, COLOR_WHITE
from code.system.dbproxy import DBProxy


def get_formatted_date():
    current_datetime = datetime.now()
    return current_datetime.strftime("%H:%M %d/%m/%y")


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = AssetManager.get_image("ScoreBg.png")

    def show(self):
        audio = AudioController()
        audio.play_music("menu")  # Toca a mesma música do menu

        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        font_title = AssetManager.get_font("VT323-Regular.ttf", 48)
        font_label = AssetManager.get_font("VT323-Regular.ttf", 20)

        while True:
            # Redimensionar fundo conforme janela
            w, h = self.window.get_size()
            surf_scaled = pygame.transform.scale(self.surf, (w, h))
            self.window.blit(surf_scaled, (0, 0))

            self.draw_text("TOP 10 SCORE", font_title, COLOR_PINK, w // 2, int(h * 0.1), center=True)
            self.draw_text("NAME     SCORE       DATE", font_label, COLOR_WHITE, w // 2, int(h * 0.2), center=True)

            for i, (id_, name, score, date) in enumerate(list_score):
                text = f"{name:<8} {int(score):05d}   {date}"
                self.draw_text(text, font_label, COLOR_WHITE, w // 2, int(h * 0.26) + i * 28, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in MENU_KEYS["back"]:
                    return

            pygame.display.flip()

    def draw_text(self, text: str, font: Font, color: tuple, x: int, y: int, center=False):
        text_surf: Surface = font.render(text, True, color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=(x, y) if center else (0, 0))
        if not center:
            text_rect.topleft = (x, y)
        self.window.blit(text_surf, text_rect)
