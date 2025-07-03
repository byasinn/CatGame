import pygame
from code.settings.settingsmanager import SettingsManager
from code.system.managers.assetmanager import AssetManager
from code.system.config import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK

# Lista de resoluções disponíveis
RESOLUTIONS = [
    (640, 360),
    (854, 480),
    (960, 540),
    (1024, 576),
    (1280, 720),  # HD
    (1366, 768),
    (1600, 900),
    (1920, 1080),  # Full HD
]

def apply_resolution():
    """Aplica resolução com base nas configurações salvas."""
    fullscreen = SettingsManager.get("fullscreen")
    res_index = SettingsManager.get("resolution_index")
    width, height = RESOLUTIONS[res_index]

    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if fullscreen:
        flags |= pygame.FULLSCREEN

    return pygame.display.set_mode((width, height), flags)

def set_resolution(index: int):
    """Define a resolução escolhida."""
    index = max(0, min(index, len(RESOLUTIONS) - 1))
    SettingsManager.set("resolution_index", index)

def toggle_fullscreen():
    """Alterna entre fullscreen e janela."""
    current = SettingsManager.get("fullscreen")
    SettingsManager.set("fullscreen", not current)

def run(window):
    selected = SettingsManager.get("resolution_index")
    fullscreen = SettingsManager.get("fullscreen")
    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        _text(window, 40, "Tela", COLOR_PINK, (window.get_width() // 2, 60), True)

        for i, (w, h) in enumerate(RESOLUTIONS):
            color = COLOR_YELLOW if i == selected else COLOR_WHITE
            _text(window, 24, f"{w}x{h}", color, (window.get_width() // 2, 140 + i * 30))

        mode = "Tela Cheia" if fullscreen else "Janela"
        _text(window, 24, f"Modo: {mode}", COLOR_WHITE, (window.get_width() // 2, 240))
        _text(window, 18, "[ENTER] Aplicar | [F] Tela cheia | ESC", COLOR_WHITE, (window.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(RESOLUTIONS)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(RESOLUTIONS)
                elif event.key == pygame.K_RETURN:
                    set_resolution(selected)
                    apply_resolution()
                    return
                elif event.key == pygame.K_f:
                    toggle_fullscreen()
                    apply_resolution()
                    return
                elif event.key == pygame.K_ESCAPE:
                    return
        clock.tick(60)

def _text(window, size, text, color, center, is_title=False):
    font_name = "PressStart2P-Regular" if is_title else "VT323-Regular"
    font = AssetManager.get_font(font_name, size)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(center=center)
    window.blit(surf, rect)