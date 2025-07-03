import random
import pygame
from code.DrawableEntity.MovingEntity.background import Background, BackgroundFloat
from code.DrawableEntity.StaticEntity.backgroundlight import BackgroundLight

class BackgroundFactory:
    @staticmethod
    def create(bg_type: str):
        surface = pygame.display.get_surface()
        if not surface:
            raise RuntimeError(
                "Surface não disponível ao criar backgrounds. Verifique se apply_resolution() foi chamado.")

        width, height = surface.get_size()
        list_bg = []

        if bg_type == "Level1":
            for i in range(6):
                bg = Background(f'Level1Bg{i}', (0, 0))
                list_bg.extend([
                    bg,
                    Background(f'Level1Bg{i}', (bg.rect.width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level1", (0, 0)))

        elif bg_type == "Level1_2":
            for i in range(3):
                bg = Background(f'Level1_2Bg{i}', (0, 0))
                list_bg.extend([
                    bg,
                    Background(f'Level1_2Bg{i}', (bg.rect.width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level1_2", (0, 0)))

        elif bg_type == "Foreground1_2":
            # 🔹 Bg0 → contínuo
            for i in range(2):
                bg = Background(f"Foreground1_2Bg0", (i * width, 0))
                list_bg.append(bg)
            # 🔹 Bg1 → galhos esporádicos
            total_instances = random.randint(3, 5)
            current_x = width * random.randint(1, 2)
            for _ in range(total_instances):
                if random.random() < 0.5:
                    y_offset = random.randint(-5, 5)
                    list_bg.append(Background(f"Foreground1_2Bg1", (current_x, y_offset)))
                current_x += width * random.randint(3, 6)

        elif bg_type == "Level2":
            for i in range(4):
                bg = Background(f'Level2Bg{i}', (0, 0))
                list_bg.extend([
                    bg,
                    Background(f'Level2Bg{i}', (bg.rect.width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level2", (0, 0)))

        elif bg_type == "Level3":
            for i in range(6):
                bg = Background(f'Level3Bg{i}', (0, 0))
                list_bg.extend([
                    bg,
                    Background(f'Level3Bg{i}', (bg.rect.width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level2", (0, 0)))

        elif bg_type == "Arcade":
            for i in range(4):
                bg = Background(f'Level1Bg{i}', (0, 0))
                list_bg.extend([
                    bg,
                    Background(f'Level1Bg{i}', (bg.rect.width, 0))
                ])
            list_bg.append(BackgroundLight("LightOverlay_Level1", (0, 0)))

        elif bg_type == "GameOver":
            for i in range(3):
                list_bg.append(BackgroundFloat(f'GameOverBg{i}', (0, 0)))
            list_bg.append(BackgroundLight("GameOverLight", (0, 0)))

        elif bg_type == "Menu":
            for i in range(4):
                list_bg.append(BackgroundFloat(f'MenuBg{i}', (0, 0)))
            list_bg.append(BackgroundLight("LightOverlay_Menu", (0, 0)))
        elif bg_type == "MenuConfig":
            for i in range(4):
                list_bg.append(BackgroundFloat(f'MenuConfig{i}', (0, 0)))
            list_bg.append(BackgroundLight("LightOverlay_MenuConfig", (0, 0)))

        return list_bg
