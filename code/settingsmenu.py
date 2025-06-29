import pygame
from pygame import Rect, Surface
from pygame.font import Font
from code.eventcontroller import EventController
from code.settings import RESOLUTIONS, RES_INDEX, FULLSCREEN, set_resolution, toggle_fullscreen, apply_resolution
from code.const import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK


class SettingsMenu:
    def __init__(self, window, audio_controller):
        self.window = window
        self.options = ["Tela", "Controles", "Voltar"]
        self.option_index = 0
        self.font_title = "./asset/PressStart2P-Regular.ttf"
        self.font_text = "./asset/VT323-Regular.ttf"
        self.audio = audio_controller

    def run(self):
        if self.audio.current_music != "menu":
            self.audio.play_music("menu")

        running = True
        while running:
            self.window.fill((0, 0, 0))
            self.draw_text(50, "CONFIGURAÇÕES", COLOR_PINK, (self.window.get_width() // 2, 70), True)

            for i, opt in enumerate(self.options):
                color = COLOR_YELLOW if i == self.option_index else COLOR_WHITE
                self.draw_text(22, opt, color, (self.window.get_width() // 2, 160 + i * 30), False)

            pygame.display.flip()

            event_list = pygame.event.get()
            result = self.handle_events_main(event_list)
            if result == "back":
                running = False

    def handle_events_main(self, event_list):
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
                    if self.option_index == 0:
                        self.run_screen_settings()
                    elif self.option_index == 1:
                        self.run_control_settings()
                    elif self.option_index == 2:
                        return "back"
                elif event.key == pygame.K_ESCAPE:
                    return "back"

    def handle_events_screen_settings(self, event_list, selected):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(RESOLUTIONS)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(RESOLUTIONS)
                elif event.key == pygame.K_RETURN:
                    set_resolution(selected)
                    self.window = apply_resolution()
                    return "applied"
                elif event.key == pygame.K_f:
                    toggle_fullscreen()
                    self.window = apply_resolution()
                    return "applied"
                elif event.key == pygame.K_ESCAPE:
                    return "back"
        return selected

    def run_screen_settings(self):
        selected = RES_INDEX

        while True:
            self.window.fill((0, 0, 0))
            self.draw_text(36, "Tela", COLOR_PINK, (self.window.get_width() // 2, 60), True)

            for i, res in enumerate(RESOLUTIONS):
                txt = f"{res[0]}x{res[1]}"
                color = COLOR_YELLOW if i == selected else COLOR_WHITE
                self.draw_text(22, txt, color, (self.window.get_width() // 2, 120 + i * 30))

            fs_text = f"Modo: {'Tela Cheia' if FULLSCREEN else 'Janela'}"
            self.draw_text(22, fs_text, COLOR_WHITE, (self.window.get_width() // 2, 260))
            self.draw_text(18, "[ENTER] Aplicar | [F] Tela cheia | [ESC] Voltar", COLOR_WHITE, (self.window.get_width() // 2, 300))

            pygame.display.flip()

            event_list = pygame.event.get()
            result = self.handle_events_screen_settings(event_list, selected)

            if result == "back":
                return
            elif result == "applied":
                return
            elif isinstance(result, int):
                selected = result

    def run_control_settings(self):
        self.window.fill((0, 0, 0))
        self.draw_text(36, "Controles", COLOR_PINK, (self.window.get_width() // 2, 80), True)
        self.draw_text(22, "A alteração de teclas será implementada em breve", COLOR_WHITE, (self.window.get_width() // 2, 150))
        self.draw_text(18, "[ESC] Voltar", COLOR_WHITE, (self.window.get_width() // 2, 240))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False

    def draw_text(self, size, text, color, center, is_title=False):
        font_path = self.font_title if is_title else self.font_text
        font = pygame.font.Font(font_path, size)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(center=center)
        self.window.blit(surf, rect)
