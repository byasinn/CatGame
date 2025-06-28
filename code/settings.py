import pygame

# ====== RESOLUÇÃO E TELA ======
WIN_WIDTH = 576
WIN_HEIGHT = 324
FULLSCREEN = False

# Lista de resoluções suportadas
RESOLUTIONS = [
    (576, 324),
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1366, 768),
    (1920, 1080),
]
RES_INDEX = 0  # índice da resolução atual

def set_resolution(index):
    global WIN_WIDTH, WIN_HEIGHT, RES_INDEX
    RES_INDEX = index % len(RESOLUTIONS)
    WIN_WIDTH, WIN_HEIGHT = RESOLUTIONS[RES_INDEX]

def toggle_fullscreen():
    global FULLSCREEN
    FULLSCREEN = not FULLSCREEN

def apply_resolution():
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN
    return pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags)
