import pygame

from code.system.managers.assetmanager import AssetManager
from code.system.config import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK

CONTROLS = {
    "Player 1": [
        ("Mover", "W A S D"),
        ("Atirar", "Espaço"),
    ],
    "Player 2": [
        ("Mover", "Setas"),
        ("Atirar", "Enter"),
    ],
}

def run(window):
    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        _text(window, 40, "Controles", COLOR_PINK, (window.get_width() // 2, 60), True)

        y = 120
        for player, binds in CONTROLS.items():
            _text(window, 26, player, COLOR_YELLOW, (window.get_width() // 2, y))
            y += 30
            for action, keys in binds:
                _text(window, 20, f"{action}: {keys}", COLOR_WHITE, (window.get_width() // 2, y))
                y += 25
            y += 15

        _text(window, 18, "[ESC] Voltar", COLOR_WHITE, (window.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        clock.tick(60)

def _text(window, size, text, color, center, is_title=False):
    font_name = "PressStart2P-Regular" if is_title else "VT323-Regular"
    font = AssetManager.get_font(font_name, size)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(center=center)
    window.blit(surf, rect)
