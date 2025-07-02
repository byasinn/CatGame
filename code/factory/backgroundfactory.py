import random

import pygame
from code.DrawableEntity.MovingEntity.background import Background, BackgroundFloat
from code.DrawableEntity.StaticEntity.backgroundlight import BackgroundLight

class BackgroundFactory:
    @staticmethod
    def create(bg_type: str):
        width = pygame.display.get_surface().get_width()
        list_bg = []

        if bg_type == "Level1":
            for i in range(6):
                list_bg.extend([
                    Background(f'Level1Bg{i}', (0, 0)),
                    Background(f'Level1Bg{i}', (width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level1", (0, 0)))

        elif bg_type == "Level1_2":
            for i in range(3):
                list_bg.extend([
                    Background(f'Level1_2Bg{i}', (0, 0)),
                    Background(f'Level1_2Bg{i}', (width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level1_2", (0, 0)))

        elif bg_type == "Foreground1_2":
            width = pygame.display.get_surface().get_width()
            # 🔹 Bg0 → contínuo
            for i in range(2):
                list_bg.append(Background(f"Foreground1_2Bg0", (i * width, 0)))
            # 🔹 Bg1 → galhos esporádicos
            total_instances = random.randint(3, 5)
            current_x = width * random.randint(1, 2)  # aparece cedo (1–2 telas)
            for _ in range(total_instances):
                if random.random() < 0.5:
                    y_offset = random.randint(-5, 5)
                    list_bg.append(Background(f"Foreground1_2Bg1", (current_x, y_offset)))
                current_x += width * random.randint(3, 6)  # espaçamento realista (5–10s)

        elif bg_type == "Level2":
            for i in range(4):
                list_bg.extend([
                    Background(f'Level2Bg{i}', (0, 0)),
                    Background(f'Level2Bg{i}', (width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level2", (0, 0)))

        elif bg_type == "Level3":
            for i in range(6):
                list_bg.extend([
                    Background(f'Level3Bg{i}', (0, 0)),
                    Background(f'Level3Bg{i}', (width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level2", (0, 0)))

        elif bg_type == "Arcade":
            for i in range(4):
                list_bg.extend([
                    Background(f'Level1Bg{i}', (0, 0)),
                    Background(f'Level1Bg{i}', (width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level1", (0, 0)))

        elif bg_type == "GameOver":
            for i in range(3):
                list_bg.extend([
                    Background(f'GameOverBg{i}', (0, 0)),
                    Background(f'GameOverBg{i}', (width, 0))
                ])
            list_bg.append(BackgroundLight("GameOverLight", (0, 0)))

        elif bg_type == "Menu":
            for i in range(4):  # ou mais camadas, se quiser
                list_bg.append(BackgroundFloat(f'MenuBg{i}', (0, 0)))
            list_bg.append(BackgroundLight("LightOverlay_Menu", (0, 0)))

        return list_bg
