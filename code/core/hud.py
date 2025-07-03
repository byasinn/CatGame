import math
import pygame
from pygame import Surface
from code.system.config import COLOR_WHITE, COLOR_PINK, COLOR_YELLOW
from code.system.managers.assetmanager import AssetManager

class HUDRenderer:
    def __init__(self, window: Surface):
        self.window = window
        self.font_cache = {}
        self.heart_img = AssetManager.get_image("Heart.png")
        self.heart_img = pygame.transform.scale(self.heart_img, (20, 20))  # reduzido para novo HUD fino
        self.cat_heads = {
            "Player1": AssetManager.get_image("Player1Head.png"),
            "Player2": AssetManager.get_image("Player2Head.png"),
            "Team": AssetManager.get_image("TeamHead.png"),
            "Player1Competitive": AssetManager.get_image("Player1Competitive.png"),
            "Player2Competitive": AssetManager.get_image("Player2Competitive.png"),
        }
        self.last_scores = {"Player1": 0, "Player2": 0}

    def draw_text(self, size: int, text: str, color: tuple, pos: tuple, is_title: bool = False):
        font_file = "PressStart2P-Regular.ttf" if is_title else "VT323-Regular.ttf"
        font = AssetManager.get_font(font_file, size)
        text_surf = font.render(text, True, color).convert_alpha()
        text_rect = text_surf.get_rect(left=pos[0], top=pos[1])
        self.window.blit(text_surf, text_rect)

    def draw_hud(self, players: list, level_name: str, timeout: int, boss_summoned: bool, fps: float, entity_count: int):
        # Novo HUD mais fino (altura menor)
        hud_bg = pygame.Surface((320, 60), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 90))  # mais translúcido
        self.window.blit(hud_bg, (5, 5))

        # Vida e score
        for i, p in enumerate(players):
            x = 10
            y = 20 + i * 22  # reposicionado para caber
            color = COLOR_PINK if p.name == "Player1" else COLOR_YELLOW
            name = "Mora" if p.name == "Player1" else "Leon"

            hearts = max(0, min(5, p.health // 200))
            for h in range(hearts):
                self.window.blit(self.heart_img, (x + h * 22, y))

        # Barra de progresso (timeout como "avanço")
        if not (level_name == "Level3" and boss_summoned):
            bar_x, bar_y, bar_w, bar_h = 10, 8, 150, 6
            percent = max(0, min(1, timeout / 30000))
            filled = int(bar_w * percent)

            pygame.draw.rect(self.window, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
            pygame.draw.rect(self.window, (255, 160, 200), (bar_x, bar_y, filled, bar_h), border_radius=3)

        # Nome do level (fonte gordinha)
        self.draw_text(13, f'{level_name}', COLOR_WHITE, (180, 7), is_title=True)

    def draw_score(self, game_mode: str, player_score: list[int], tick: int):
        x_base = 350
        y_base = 5
        shake = lambda t: int(math.sin(t * 0.3) * 2)

        def draw_icon_score(img_key, score, x, y, highlight=False, animate=False):
            now = pygame.time.get_ticks()
            scale = 1.0

            if animate:
                scale = 1.0 + 0.1 * math.sin(now * 0.02)  # cresce e volta suavemente

            # Redimensiona a imagem da cabeça com "bounce"
            img_raw = self.cat_heads[img_key]
            img_size = int(32 * scale)
            img = pygame.transform.scale(img_raw, (img_size, img_size))

            img_rect = img.get_rect(center=(x + 16, y + 16))  # centraliza

            color = (255, 50, 50) if highlight else COLOR_WHITE
            score_text = f"{score}" if score > 0 else "0"

            self.window.blit(img, img_rect.topleft)
            self.draw_text(18, score_text, color, (x + 40, y + 5), is_title=True)

        if game_mode == "Solo":
            score = player_score[0]
            diff = score - self.last_scores["Player1"]
            animate = diff > 0
            self.last_scores["Player1"] = score

            draw_icon_score("Player1", score, x_base, y_base, animate=animate)

        elif game_mode == "Coop":
            score = int((player_score[0] + player_score[1]) / 2)
            diff = score - self.last_scores["Player1"]
            animate = diff > 0
            self.last_scores["Player1"] = score

            draw_icon_score("Team", score, x_base, y_base, animate=animate)

        elif game_mode == "Versus":
            s1, s2 = player_score
            self.last_scores["Player1"] = s1
            self.last_scores["Player2"] = s2

            higher = 0 if s1 >= s2 else 1
            for i, name in enumerate(["Player1", "Player2"]):
                score = player_score[i]
                img_key = f"{name}Competitive"
                is_winner = i == higher and score > 0
                draw_icon_score(img_key, score, x_base, y_base + i * 35, highlight=is_winner, animate=is_winner)

    def draw_tutorial_message(self, surface, text: str, darken: bool = True, blink: bool = True):
        if darken:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))

        if blink:
            alpha = int(255 * abs(math.sin(pygame.time.get_ticks() * 0.002)))
        else:
            alpha = 255

        font = AssetManager.get_font("PressStart2P-Regular", 16)
        msg_surface = font.render(text, True, (255, 255, 255))
        msg_surface.set_alpha(alpha)
        rect = msg_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 4))
        surface.blit(msg_surface, rect)

