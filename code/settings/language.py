import pygame
from code.system.config import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK
from code.settings.settingsmanager import SettingsManager

LANGUAGES = [("pt", "Português"), ("en", "English")]

def run(window):
    selected = 0
    current = SettingsManager.get("language") or "pt"
    codes = [lang[0] for lang in LANGUAGES]
    labels = [lang[1] for lang in LANGUAGES]

    if current in codes:
        selected = codes.index(current)

    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        _text(window, 40, "Idioma", COLOR_PINK, (window.get_width() // 2, 70), True)

        for i, lang_label in enumerate(labels):
            color = COLOR_YELLOW if i == selected else COLOR_WHITE
            _text(window, 28, lang_label, color, (window.get_width() // 2, 150 + i * 40))

        _text(window, 18, "ENTER para escolher | ESC para voltar", COLOR_WHITE, (window.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(LANGUAGES)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(LANGUAGES)
                elif event.key == pygame.K_RETURN:
                    SettingsManager.set("language", codes[selected])
                    pygame.time.wait(300)  # (opcional) pequena pausa
                    return
                elif event.key == pygame.K_ESCAPE:
                    return
        clock.tick(60)

def _text(window, size, text, color, center, is_title=False):
    font_path = "./asset/PressStart2P-Regular.ttf" if is_title else "./asset/VT323-Regular.ttf"
    font = pygame.font.Font(font_path, size)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(center=center)
    window.blit(surf, rect)
