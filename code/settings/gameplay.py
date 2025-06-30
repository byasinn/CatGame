import pygame
from code.system.config import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK
from code.settings.settingsmanager import SettingsManager

OPTIONS = [
    ("Efeitos Visuais", "visual_effects"),
    ("Sangue/Gore", "gore"),
]

def run(window):
    selected = 0
    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        _text(window, 40, "Gameplay", COLOR_PINK, (window.get_width() // 2, 60), True)

        for i, (label, key) in enumerate(OPTIONS):
            enabled = SettingsManager.get(key)
            color = COLOR_YELLOW if i == selected else COLOR_WHITE
            status = "Ativado" if enabled else "Desativado"
            _text(window, 26, f"{label}: {status}", color, (window.get_width() // 2, 140 + i * 40))

        _text(window, 18, "ENTER para alternar | ESC para voltar", COLOR_WHITE, (window.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(OPTIONS)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(OPTIONS)
                elif event.key == pygame.K_RETURN:
                    label, key = OPTIONS[selected]
                    current = SettingsManager.get(key)
                    SettingsManager.set(key, not current)
                elif event.key == pygame.K_ESCAPE:
                    return
        clock.tick(60)

def _text(window, size, text, color, center, is_title=False):
    font_path = "./asset/PressStart2P-Regular.ttf" if is_title else "./asset/VT323-Regular.ttf"
    font = pygame.font.Font(font_path, size)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(center=center)
    window.blit(surf, rect)
