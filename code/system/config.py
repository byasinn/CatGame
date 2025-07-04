# config.py
import pygame

# 🎨 Cores
COLOR_PINK = (255, 182, 193)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)

# 🎮 Eventos customizados
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2

# 🧠 Entidades
ENTITY_STATS = {
    # Jogadores
    "Player1":       {"speed": 4, "health": 1000, "damage": 1,  "score": 0, "shot_delay": 20},
    "Player1Shot":   {"speed": 9,   "health": 1,    "damage": 25, "score": 0},
    "Player2":       {"speed": 4,   "health": 1000, "damage": 1,  "score": 0, "shot_delay": 20},
    "Player2Shot":   {"speed": 9,   "health": 1,    "damage": 25, "score": 0},

    # Inimigos
    "Enemy1":        {"speed": 4,   "health": 50,   "damage": 1,  "score": 100, "shot_delay": 20},
    "Enemy1Shot":    {"speed": 5,   "health": 1,    "damage": 20, "score": 0},
    "Enemy2":        {"speed": 3,   "health": 60,   "damage": 1,  "score": 125, "shot_delay": 20},
    "Enemy2Shot":    {"speed": 3,   "health": 1,    "damage": 20, "score": 0},
    "Enemy3":        {"speed": 2,   "health": 60,   "damage": 1,  "score": 125, "shot_delay": 20},
    "Enemy3Shot":    {"speed": 3,   "health": 1,    "damage": 20, "score": 0},
    "EnemyTest":     {"speed": 0,   "health": 5,    "damage": 0,  "score": 0, "shot_delay": 100},
    "EnemyTestShot": {"speed": 1,   "health": 1,    "damage": 0,  "score": 0},

    # Boss
    "Boss":          {"speed": 2,   "health": 500,  "damage": 1,  "score": 1000, "shot_delay": 40},
    "BossShot":      {"speed": 6,   "health": 1,    "damage": 30, "score": 0},

    # 🎨 Foregrounds com velocidade fixa
    "Foreground1_2Bg0": {"speed": 3, "health": 999, "damage": 0, "score": 0},
    "Foreground1_2Bg1": {"speed": 3, "health": 999, "damage": 0, "score": 0},
    'MenuConfig0': {"speed": 0, "health": 999, "damage": 0, "score": 0},
    'MenuConfig1': {"speed": 4, "health": 999, "damage": 0, "score": 0},
    'MenuConfig2': {"speed": 3, "health": 999, "damage": 0, "score": 0},
    "MenuConfig3": {"speed": 0, "health": 999, "damage": 0, "score": 0},
}

# Overlays estáticos
for name in [
    "GameOverLight0",
    "LightOverlay_Menu0"
    "LightOverlay_MenuConfig"
    "LightOverlay_Level1_3"

]:
    ENTITY_STATS[name] = {"speed": 0, "health": 999, "damage": 0, "score": 0}

# BGs e elementos visuais (0–5 variantes)
bg_prefixes = [

    # Levels
    "Level1Bg", "Level1_2Bg", "Level1_3Bg", "BossBg",

    # Interface
    "MenuBg", "GameOverBg",

    # Scenes (corrigido)
    "Scene1_1Bg", "Scene1_2Bg", "Scene1_3Bg", "Scene1_3_2Bg", "Scene1_4Bg",
]

for prefix in bg_prefixes:
    for i in range(6):
        ENTITY_STATS[f"{prefix}{i}"] = {"speed": i if i < 6 else 0, "health": 999, "damage": 0, "score": 0}

# Geração automática
ENTITY_SPEED       = {k: v.get("speed", 0) for k, v in ENTITY_STATS.items()}
ENTITY_HEALTH      = {k: v.get("health", 999) for k, v in ENTITY_STATS.items()}
ENTITY_DAMAGE      = {k: v.get("damage", 0) for k, v in ENTITY_STATS.items()}
ENTITY_SCORE       = {k: v.get("score", 0) for k, v in ENTITY_STATS.items()}
ENTITY_SHOT_DELAY  = {k: v["shot_delay"] for k, v in ENTITY_STATS.items() if "shot_delay" in v}

# 🕹️ Menu e Tempo
MENU_OPTION = ("NEW GAME", "SCORE", "SETTINGS", "EXIT")
TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 20000

# ⌨️ Teclas de controle
PLAYER_KEY_UP = {"Player1": pygame.K_UP, "Player2": pygame.K_w}
PLAYER_KEY_DOWN = {"Player1": pygame.K_DOWN, "Player2": pygame.K_s}
PLAYER_KEY_LEFT = {"Player1": pygame.K_LEFT, "Player2": pygame.K_a}
PLAYER_KEY_RIGHT = {"Player1": pygame.K_RIGHT, "Player2": pygame.K_d}
PLAYER_KEY_SHOOT = {"Player1": pygame.K_RCTRL, "Player2": pygame.K_LCTRL}

# ⏱️ Spawn e Janela
SPAWN_TIME = 4000
WIN_WIDTH = 576
WIN_HEIGHT = 324

# 🏆 Posição dos scores
SCORE_POS = {
    'Title': (WIN_WIDTH / 2, 50),
    'EnterName': (WIN_WIDTH / 2, 80),
    'Label': (WIN_WIDTH / 2, 90),
    'Name': (WIN_WIDTH / 2, 110),
    **{i: (WIN_WIDTH / 2, 110 + i * 20) for i in range(10)}
}
