import pygame
import sys
from pygame import Surface
from code.system.managers.assetmanager import AssetManager
from code.settings.lang import t

class FinishLevel:
    def __init__(self, window: Surface, level_name: str):
        self.window = window
        self.level_name = level_name
        self.clock = pygame.time.Clock()

    def run(self):
        font = AssetManager.get_font("VT323-Regular", 32)
        while True:
            self.clock.tick(60)
            self.window.fill((0, 0, 0))

            text1 = font.render(f"{t('level_completed')}: {self.level_name}", True, (255, 255, 255))
            text2 = font.render(t("press_enter_continue"), True, (200, 200, 200))
            text3 = font.render(t("press_esc_menu"), True, (200, 200, 200))

            w, h = self.window.get_size()
            self.window.blit(text1, text1.get_rect(center=(w // 2, h * 0.3)))
            self.window.blit(text2, text2.get_rect(center=(w // 2, h * 0.5)))
            self.window.blit(text3, text3.get_rect(center=(w // 2, h * 0.6)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        return False
