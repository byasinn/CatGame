import pygame
from pygame import Surface
from code.factory.backgroundfactory import BackgroundFactory
from code.system.managers.assetmanager import AssetManager
from code.system.config import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK
from code.settings import display, audio, gameplay, language, controls
from code.settings.lang import t
from code.system.particle import draw_grain_overlay


class SettingsMenu:
    def __init__(self, window: Surface, audio_controller):
        self.window = window
        self.audio = audio_controller
        self.option_keys = ["screen", "audio", "language", "controls", "gameplay", "back"]
        self.options = [t(key) for key in self.option_keys]
        self.option_index = 0
        self.bg_list = BackgroundFactory.create("MenuConfig")

    def run(self):
        running = True
        if self.audio.current_music != "menu":
            self.audio.play_music("menu")

        while running:
            for bg in self.bg_list:
                bg.move()
                self.window.blit(bg.surf, bg.rect)
            self.draw_text(50, "CONFIGURAÇÕES", COLOR_PINK, (self.window.get_width() // 2, 70), True)
            draw_grain_overlay(self.window)

            for i, opt in enumerate(self.options):
                color = COLOR_YELLOW if i == self.option_index else COLOR_WHITE
                self.draw_text(22, opt, color, (self.window.get_width() // 2, 160 + i * 30), False)

            pygame.display.flip()
            event_list = pygame.event.get()
            running = not self.handle_events(event_list)

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.option_index = (self.option_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.option_index = (self.option_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.select_option()
                elif event.key == pygame.K_ESCAPE:
                    return True
        return False

    def select_option(self):
        key = self.option_keys[self.option_index]
        if key == "screen":
            display.run(self.window)
        elif key == "audio":
            audio.run(self.window)
        elif key == "language":
            language.run(self.window)

            # Após voltar do menu de idioma, recarrega labels traduzidas
            self.options = [t("screen"), t("audio"), t("language"), t("controls"), t("gameplay"), t("back")]

        elif key == "controls":
            controls.run(self.window)
        elif key == "gameplay":
            gameplay.run(self.window)
        elif key == "back":
            return True
        return False

    def draw_text(self, size, text, color, center, is_title=False):
        font_name = "PressStart2P-Regular" if is_title else "VT323-Regular"
        font = AssetManager.get_font(font_name, size)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(center=center)
        self.window.blit(surf, rect)
