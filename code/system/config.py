# C
import pygame
from pygame.examples.grid import WINDOW_WIDTH

COLOR_PINK = (255, 182, 193)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)

#E

EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
ENTITY_SPEED = {
    'LightOverlay_Level1': 0,
    'Level1Bg0' : 0,
    'Level1Bg1' : 1,
    'Level1Bg2' : 2,
    'Level1Bg3' : 3,
    'Level1Bg4' : 4,
    'Level1Bg5' : 5,
    'Level1Bg6' : 6,

    'Level1_2Bg0': 0,
    'Level1_2Bg1': 1,
    'Level1_2Bg2': 2,
    'LightOverlay_Level1_2': 0,
    "Foreground1_2Bg0": 7,
    "Foreground1_2Bg1": 3,

    "Player1": 3.5,
    "Player1Shot": 7,
    "Player2": 3,
    "Player2Shot": 6,
    "Enemy1": 2,
    "Enemy1Shot": 5,
    "Enemy2": 2,
    "Enemy2Shot": 3,
    "EnemyTest": 0,
    "EnemyTestShot": 1,

    'Level2Bg0': 0,
    'Level2Bg1': 1,
    'Level2Bg2': 2,
    'Level2Bg3': 3,

    'Level3Bg0': 0,
    'Level3Bg1': 1,
    'Level3Bg2': 3,
    'Level3Bg3': 2,
    'Level3Bg4': 1,
    'Level3Bg5': 2,

    'Scene1_2_00': 0,
    'Scene1_2_01': 1,
    'Scene1_2_02': 2,

    'MenuBg0': 0,
    'MenuBg1': 1,
    'MenuBg2': 2,
    'MenuBg3': 3,
    'MenuBg4': 4,

    'Boss' : 2,
    'BossShot': 6,

    'GameOverBg0': 0,
    'GameOverBg1': 1,
    'GameOverBg2': 2,
    'GameOverLight': 0,

    'Scene1Bg': 0,
    'Scene1_1Bg': 1,
    'Scene1_2Bg': 2,
    'Scene1_3Bg': 1,
    'Scene1_4Bg': 2,

}

ENTITY_HEALTH = {
'LightOverlay_Level1': 999,
    'Level1Bg0' : 999,
    'Level1Bg1' : 999,
    'Level1Bg2' : 999,
    'Level1Bg3' : 999,
    'Level1Bg4' : 999,
    'Level1Bg5' : 999,
    'Level1Bg6' : 999,

    'Level1_2Bg0': 999,
    'Level1_2Bg1': 999,
    'Level1_2Bg2': 999,
    'LightOverlay_Level1_2': 999,
    "Foreground1_2Bg0": 999,
    "Foreground1_2Bg1": 999,

    "Player1": 1000,
    "Player1Shot": 1,
    "Player2": 1000,
    "Player2Shot": 1,
    "Enemy1": 50,
    "Enemy1Shot": 1,
    "Enemy2": 60,
    "Enemy2Shot": 1,
    "EnemyTest": 5,
    "EnemyTestShot": 1,

    'Level2Bg0': 999,
    'Level2Bg1': 999,
    'Level2Bg2': 999,
    'Level2Bg3': 999,

    'Level3Bg0': 999,
    'Level3Bg1': 999,
    'Level3Bg2': 999,
    'Level3Bg3': 999,
    'Level3Bg4': 999,
    'Level3Bg5': 999,

    'Scene1_2_00': 999,
    'Scene1_2_01': 999,
    'Scene1_2_02': 999,

    'MenuBg0': 999,
    'MenuBg1': 999,
    'MenuBg2': 999,
    'MenuBg3': 999,
    'MenuBg4': 999,

    'Boss': 500,
    'BossShot': 1,

    'GameOverBg0': 999,
    'GameOverBg1': 999,
    'GameOverBg2': 999,
    'GameOverLight': 999,

    'Scene1Bg': 999,
    'Scene1_1Bg': 999,
    'Scene1_2Bg': 999,
    'Scene1_3Bg': 999,
    'Scene1_4Bg': 999,

}

ENTITY_DAMAGE = {
'LightOverlay_Level1': 0,
    'Level1Bg0' : 0,
    'Level1Bg1' : 0,
    'Level1Bg2' : 0,
    'Level1Bg3' : 0,
    'Level1Bg4' : 0,
    'Level1Bg5' : 0,
    'Level1Bg6' : 0,

    'Level1_2Bg0': 0,
    'Level1_2Bg1': 0,
    'Level1_2Bg2': 0,
    'LightOverlay_Level1_2': 0,
    "Foreground1_2Bg0": 0,
    "Foreground1_2Bg1": 0,

    "Player1": 1,
    "Player1Shot": 25,
    "Player2": 1,
    "Player2Shot": 25,
    "Enemy1": 1,
    "Enemy1Shot": 20,
    "Enemy2": 1,
    "Enemy2Shot": 20,
    "EnemyTest": 0,
    "EnemyTestShot": 0,

    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,

    'Level3Bg0': 0,
    'Level3Bg1': 0,
    'Level3Bg2': 0,
    'Level3Bg3': 0,
    'Level3Bg4': 0,
    'Level3Bg5': 0,

    'Scene1_2_00': 0,
    'Scene1_2_01': 0,
    'Scene1_2_02': 0,

    'MenuBg0': 0,
    'MenuBg1': 0,
    'MenuBg2': 0,
    'MenuBg3': 0,
    'MenuBg4': 0,

    'Boss': 1,
    'BossShot': 30,

    'GameOverBg0': 0,
    'GameOverBg1': 0,
    'GameOverBg2': 0,
    'GameOverLight': 0,

    'Scene1Bg': 0,
    'Scene1_1Bg': 0,
    'Scene1_2Bg': 0,
    'Scene1_3Bg': 0,
    'Scene1_4Bg': 0,

}

ENTITY_SCORE = {
'LightOverlay_Level1': 0,
    'Level1Bg0' : 0,
    'Level1Bg1' : 0,
    'Level1Bg2' : 0,
    'Level1Bg3' : 0,
    'Level1Bg4' : 0,
    'Level1Bg5' : 0,
    'Level1Bg6' : 0,

    'Level1_2Bg0': 0,
    'Level1_2Bg1': 0,
    'Level1_2Bg2': 0,
    'LightOverlay_Level1_2': 0,
    "Foreground1_2Bg0": 0,
    "Foreground1_2Bg1": 0,

    "Player1": 0,
    "Player1Shot": 0,
    "Player2": 0,
    "Player2Shot": 0,
    "Enemy1": 100,
    "Enemy1Shot": 0,
    "Enemy2": 125,
    "Enemy2Shot": 0,
    "EnemyTest": 0,
    "EnemyTestShot": 0,

    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,

    'Level3Bg0': 0,
    'Level3Bg1': 0,
    'Level3Bg2': 0,
    'Level3Bg3': 0,
    'Level3Bg4': 0,
    'Level3Bg5': 0,

    'Scene1_2_00': 0,
    'Scene1_2_01': 0,
    'Scene1_2_02': 0,

    'MenuBg0': 0,
    'MenuBg1': 0,
    'MenuBg2': 0,
    'MenuBg3': 0,
    'MenuBg4': 0,

    'Boss': 1000,
    'BossShot': 0,

    'GameOverBg0': 0,
    'GameOverBg1': 0,
    'GameOverBg2': 0,
    'GameOverLight': 0,

    'Scene1Bg': 0,
    'Scene1_1Bg': 0,
    'Scene1_2Bg': 0,
    'Scene1_3Bg': 0,
    'Scene1_4Bg': 0,

}

ENTITY_SHOT_DELAY = {
    "Player1": 20,
    'Player2': 20,
    "Enemy1": 20,
    'Enemy2': 20,
    "EnemyTest": 100,

    'Boss': 40,
}
# M
MENU_OPTION = ("NEW GAME", "SCORE", "SETTINGS", "EXIT")


# T
TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 20000

# P
PLAYER_KEY_UP = {"Player1": pygame.K_UP,
                "Player2": pygame.K_w,}
PLAYER_KEY_DOWN = {"Player1": pygame.K_DOWN,
                   "Player2": pygame.K_s,}
PLAYER_KEY_LEFT = {"Player1": pygame.K_LEFT,
                   "Player2": pygame.K_a,}
PLAYER_KEY_RIGHT = {"Player1": pygame.K_RIGHT,
                    "Player2": pygame.K_d,}
PLAYER_KEY_SHOOT = {"Player1": pygame.K_RCTRL,
                    "Player2": pygame.K_LCTRL,}

# S
SPAWN_TIME = 4000

# W
WIN_WIDTH = 576
WIN_HEIGHT = 324

SCORE_POS = {'Title': (WIN_WIDTH / 2, 50),
             'EnterName': (WIN_WIDTH / 2, 80),
             'Label': (WIN_WIDTH / 2, 90),
             'Name': (WIN_WIDTH / 2, 110),
             0: (WIN_WIDTH / 2, 110),
             1: (WIN_WIDTH / 2, 130),
             2: (WIN_WIDTH / 2, 150),
             3: (WIN_WIDTH / 2, 170),
             4: (WIN_WIDTH / 2, 190),
             5: (WIN_WIDTH / 2, 210),
             6: (WIN_WIDTH / 2, 230),
             7: (WIN_WIDTH / 2, 250),
             8: (WIN_WIDTH / 2, 270),
             9: (WIN_WIDTH / 2, 290),
}
