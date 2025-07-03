import sys
import pygame
from code.system.managers.assetmanager import AssetManager
from code.system.controllers.audiocontroller import AudioController
from code.system.keys import CUTSCENE_KEYS
from code.system.particle import draw_grain_overlay
from code.system.visualeffects import fade

def handle_skip_and_quit(window):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [CUTSCENE_KEYS["skip"], CUTSCENE_KEYS["pause"]]:
                fade(window, fade_in=True)
                return True
    return False

def show_intro_text(window):
    font = AssetManager.get_font("VT323-Regular.ttf", 26)
    text = "be patient"
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
    draw_grain_overlay(window)

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    duration = 4000
    skipped = False

    while True:
        now = pygame.time.get_ticks() - start_time
        if now >= duration:
            break
        skipped = handle_skip_and_quit(window)
        if skipped:
            break

        window.fill((0, 0, 0))
        window.blit(text_surf, text_rect)
        pygame.display.flip()
        clock.tick(60)

    if not skipped:
        fade(window, fade_in=True)

def show_second_intro_screen(window):
    sprite_sheet = AssetManager.get_image("intro2_sprite.png")
    overlay_img = AssetManager.get_image("overlay_intro2.png")
    overlay_rect = overlay_img.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
    draw_grain_overlay(window)

    audio = AudioController()
    audio.play_music("intro2", loop=0)

    sheet_cols = 5
    sheet_rows = 4
    frame_width = sprite_sheet.get_width() // sheet_cols
    frame_height = sprite_sheet.get_height() // sheet_rows
    total_frames = sheet_cols * sheet_rows
    frame_duration = 100
    total_duration = 4000

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    skipped = False

    while True:
        now = pygame.time.get_ticks() - start_time
        if now >= total_duration:
            break

        skipped = handle_skip_and_quit(window)
        if skipped:
            break

        frame_idx = min(now // frame_duration, total_frames - 1)
        row = frame_idx // sheet_cols
        col = frame_idx % sheet_cols

        frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
        frame_surf = sprite_sheet.subsurface(frame_rect)

        window.fill((0, 0, 0))
        window.blit(pygame.transform.scale(frame_surf, window.get_size()), (0, 0))

        if now >= 1400:
            window.blit(overlay_img, overlay_rect)

        pygame.display.flip()
        clock.tick(60)

    if not skipped:
        fade(window, fade_in=True)

    audio.stop_music()

def show_intro_screen(window, audio):
    intro_img = AssetManager.get_image("IntroScreen.png")
    intro_img = pygame.transform.scale(intro_img, (window.get_width(), window.get_height()))
    draw_grain_overlay(window)

    if not pygame.mixer_music.get_busy():
        audio.play_music("intro")

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    intro_duration = 5000
    skipped = False

    while True:
        now = pygame.time.get_ticks() - start_time
        if now >= intro_duration:
            break

        skipped = handle_skip_and_quit(window)
        if skipped:
            break

        window.fill((0, 0, 0))
        alpha = min(255, int(now / 20))
        img_copy = intro_img.copy()
        img_copy.set_alpha(alpha)
        window.blit(img_copy, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    if not skipped:
        fade(window, fade_in=True)

    audio.stop_music()