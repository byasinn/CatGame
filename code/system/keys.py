import pygame

KEY_PAUSE = pygame.K_ESCAPE
KEY_SELECT = pygame.K_RETURN
KEY_BACK = pygame.K_ESCAPE

PLAYER1_KEYS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "shoot": pygame.K_SPACE,
    "power1": pygame.K_1,
    "power2": pygame.K_2,
    "power3": pygame.K_3,
    "shield": pygame.K_e,
}

PLAYER1_GAMEPAD = {
    "shoot": 0,
    "power1": 1,
    "shield": 2
}

PLAYER2_KEYS = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "shoot": pygame.K_LCTRL,
    "power1": pygame.K_0,
    "power2": pygame.K_9,
    "power3": pygame.K_8,
    "shield": pygame.K_LSHIFT,
}

PLAYER2_GAMEPAD = {
    "shoot": 0,
    "power1": 1,
    "shield": 2
}

CUTSCENE_KEYS = {
    "pause": pygame.K_ESCAPE,
    "skip": pygame.K_RETURN
}

MENU_KEYS = {
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "left": [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT],
    "select": [pygame.K_RETURN, pygame.BUTTON_LEFT],
    "back": [pygame.K_ESCAPE],
}

DEV_KEYS = {
    "level1": pygame.K_F1,
    "level2": pygame.K_F2,
    "level3": pygame.K_F3,
}
