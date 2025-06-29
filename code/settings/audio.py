import pygame
from code.const import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK
from code.settings.settingsmanager import SettingsManager
from code.audiocontroller import AudioController

def run(window):
    audio = AudioController()
    selected = 0
    options = ["Música", "Efeitos", "Voltar"]
    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        _text(window, 40, "Áudio", COLOR_PINK, (window.get_width() // 2, 60), True)

        for i, opt in enumerate(options):
            y = 140 + i * 40
            color = COLOR_YELLOW if i == selected else COLOR_WHITE
            _text(window, 24, opt, color, (window.get_width() // 2 - 100, y))

            if opt == "Música":
                vol = int(SettingsManager.get("music_volume") * 10)
                _text(window, 24, f"{vol}/10", color, (window.get_width() // 2 + 50, y))
            elif opt == "Efeitos":
                vol = int(SettingsManager.get("sfx_volume") * 10)
                _text(window, 24, f"{vol}/10", color, (window.get_width() // 2 + 50, y))

        _text(window, 18, "← → para ajustar | ESC para voltar", COLOR_WHITE, (window.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_LEFT:
                    _adjust_volume(audio, selected, -0.1)
                elif event.key == pygame.K_RIGHT:
                    _adjust_volume(audio, selected, 0.1)
                elif event.key == pygame.K_ESCAPE:
                    return
        clock.tick(60)

def _adjust_volume(audio: AudioController, selected: int, delta: float):
    if selected == 0:
        new_vol = round(min(1.0, max(0.0, SettingsManager.get("music_volume") + delta)), 2)
        SettingsManager.set("music_volume", new_vol)
        audio.set_music_volume(new_vol)
    elif selected == 1:
        new_vol = round(min(1.0, max(0.0, SettingsManager.get("sfx_volume") + delta)), 2)
        SettingsManager.set("sfx_volume", new_vol)
        audio.set_sfx_volume(new_vol)

def _text(window, size, text, color, center, is_title=False):
    font_path = "./asset/PressStart2P-Regular.ttf" if is_title else "./asset/VT323-Regular.ttf"
    font = pygame.font.Font(font_path, size)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(center=center)
    window.blit(surf, rect)
