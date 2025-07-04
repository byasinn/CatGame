from code.settings.settingsmanager import SettingsManager

LANG_DICT = {
    "pt": {
        # Menu principal
        "title_main1": "Mora",
        "title_main2": "Migos",
        "new_game": "NOVO JOGO",
        "score": "PLACAR",
        "settings": "CONFIGURAÇÕES",
        "exit": "SAIR",

        # Submenus
        "screen": "Tela",
        "audio": "Áudio",
        "language": "Idioma",
        "controls": "Controles",
        "gameplay": "Efeitos Visuais",
        "back": "Voltar",
        "settings_title": "CONFIGURAÇÕES",

        # Opções de modos
        "mode_select_title": "Tipo de Jogo",
        "campaign": "Campanha",
        "arcade": "Arcade",
        "solo": "Solo",
        "cooperative": "Cooperativo",
        "competitive": "Competitivo",

        "load_game_title": "Carregar Jogo",
        "load_game": "CARREGAR JOGO",
        "empty_slot": "Vazio",
        "level_completed": "Fase Concluída",
        "press_enter_continue": "Pressione ENTER para continuar",
        "press_esc_menu": "Pressione ESC para voltar ao menu",

        # Gameplay e dicas
        "visual_effects_enabled": "Ativado",
        "visual_effects_disabled": "Desativado",
        "apply_instruction": "ENTER para alternar | ESC para voltar",

        # Idioma
        "language_select_title": "Idioma",
        "enter_to_select": "ENTER para escolher | ESC para voltar",

        # Controles
        "controls_title": "Controles",
        "move": "Mover",
        "shoot": "Atirar",
        "player1": "Player 1",
        "player2": "Player 2",
        "back_hint": "[ESC] Voltar",

        # HUD / Nomes
        "hud_mora": "Mora",
        "hud_leon": "Leon",

        # Game Over
        "game_over": "Game Over",

        # Score
        "score_title": "TOP 10 PLACAR",
        "score_header": "NOME     PONTOS     DATA",
        "score_win": "GATINHOS WIN!",
        "score_enter_name": "Digite seu nome",
        "score_enter_team": "Digite o nome da equipe",
        "score_player1_enter": "Player 1, digite seu nome",
        "score_player2_enter": "Player 2, digite seu nome",

        # Scene
        "scenes1": [
            {"background": ["Scene1_1Bg0", "Scene1_1Bg1"], "characters": [], "text": "Leon: Está um silêncio estranho por aqui..."},
            {"background": ["Scene1_1Bg2"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Será que Mora já chegou?"},
            {"background": ["Scene1_1Bg2"], "characters": [("Mora", "right", "fadein")], "text": "Mora: Estou aqui! Não se assuste!"},
            {"background": ["Scene1_1Bg3"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Que bom!"},
            {"background": ["Scene1_1Bg4"], "characters": [("Mora", "right", "fadein")], "text": "Mora: Vamos lá!"}
        ],

        "scenes2": [
            {"background": ["Scene1_2Bg0", "Scene1_2Bg1", "Scene1_2Bg2"], "characters": [], "text": "Leon: Finalmente, chegamos à floresta...", "music": "Scene2.mp3"},
            {"characters": [("Mora", "right", "fadein")], "text": "Mora: Foi difícil, mas conseguimos..."},
            {"characters": [("Leon", "left", "fadein")], "text": "Leon: Ainda não acredito no que enfrentamos."},
            {"characters": [("Luri", "right", "fadein")], "text": "Luri: Ainda bem que vocês chegaram!"},
            {"characters": [("Leon", "left", "fadein")], "text": "Leon: Luri!? Onde você estava?"},
            {"characters": [("Mora", "right", "fadein")], "text": "Mora: A gente precisava de você lá atrás!"},
            {"characters": [("Luri_rindo", "right", "fadein")], "text": "Luri: Hehe... Eu tava... ocupado... com borboletas."},
            {"characters": [("Luri_assustado", "right", "fadein")], "text": "Luri: ESPERA... vocês ouviram isso?"},
            {"characters": [("Enemy", "left", "fadein")], "text": "??? : Grrrraaahhh..."},
            {"characters": [("Leon_bravo", "left", "fadein")], "text": "Leon: VOCÊ DE NOVO?!"},
            {"characters": [("Mora_brava", "right", "fadein")], "text": "Mora: Não vamos fugir dessa vez!"},
            {"characters": [("Enemy", "left", "fadein")], "text": "??? : Acabou para vocês..."},
            {"characters": [("Luri_assustado", "right", "fadein")], "text": "Luri: Eu... eu protejo a retaguarda!"},
            {"characters": [("Leon_bravo", "left", "fadein")], "text": "Leon: Se preparem!"}
        ],

        "scenes3": [
            {"background": ["Scene1_3Bg0", "Scene1_3Bg1", "Scene1_3Bg2", "Scene1_3Bg3"], "characters": [], "text": "Mora: Estamos quase lá...", "music": "Scene3.mp3"},
            {"background": ["Scene1_3_2Bg0"], "characters": [("Mora", "left", "fadein"), ("Luri", "right", "fadein")], "text": "Luri: Finalmente vocês chegaram..."},
        ],

        "scenes4": [
            {"background": ["Scene1_3Bg0", "Scene1_3Bg1", "Scene1_3Bg2", "Scene1_3Bg3"], "characters": [], "text": "Mora: Estamos quase lá...", "music": "Scene3.mp3"},
            {"background": ["Scene1_3_2Bg0"], "characters": [("Mora", "left", "fadein"), ("Luri", "right", "fadein")], "text": "Luri: Finalmente vocês chegaram..."},
        ],
    },






    "en": {
        # Main menu
        "title_main1": "Mora",
        "title_main2": "Migos",
        "new_game": "NEW GAME",
        "score": "SCORE",
        "settings": "SETTINGS",
        "exit": "EXIT",

        # Submenus
        "screen": "Display",
        "audio": "Audio",
        "language": "Language",
        "controls": "Controls",
        "gameplay": "Visual Effects",
        "back": "Back",
        "settings_title": "SETTINGS",

        # Game modes
        "mode_select_title": "Game Type",
        "campaign": "Campaign",
        "arcade": "Arcade",
        "solo": "Solo",
        "cooperative": "Cooperative",
        "competitive": "Competitive",

        "load_game_title": "Load Game",
        "load_game": "LOAD GAME",
        "empty_slot": "Empty",
        "level_completed": "Level Completed",
        "press_enter_continue": "Press ENTER to continue",
        "press_esc_menu": "Press ESC to return to menu",

        # Gameplay and hints
        "visual_effects_enabled": "Enabled",
        "visual_effects_disabled": "Disabled",
        "apply_instruction": "ENTER to toggle | ESC to go back",

        # Language
        "language_select_title": "Language",
        "enter_to_select": "ENTER to choose | ESC to go back",

        # Controls
        "controls_title": "Controls",
        "move": "Move",
        "shoot": "Shoot",
        "player1": "Player 1",
        "player2": "Player 2",
        "back_hint": "[ESC] Back",

        # HUD
        "hud_mora": "Mora",
        "hud_leon": "Leon",

        # Game Over
        "game_over": "Game Over",

        # Score
        "score_title": "TOP 10 SCORES",
        "score_header": "NAME     SCORE      DATE",
        "score_win": "CATS WIN!",
        "score_enter_name": "Enter your name",
        "score_enter_team": "Enter team name",
        "score_player1_enter": "Player 1, enter your name",
        "score_player2_enter": "Player 2, enter your name",

        #Scenes
        "scenes1": [
            {"background": ["Scene1_1Bg0", "Scene1_1Bg1"], "characters": [], "text": "Leon: It's oddly quiet around here..."},
            {"background": ["Scene1_1Bg2"], "characters": [("Leon", "left", "fadein")], "text": "Leon: I wonder if Mora's already here?"},
            {"background": ["Scene1_1Bg2"], "characters": [("Mora", "right", "fadein")], "text": "Mora: I'm here! Don't be scared!"},
            {"background": ["Scene1_1Bg3"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Good to see you!"},
            {"background": ["Scene1_1Bg4"], "characters": [("Mora", "right", "fadein")], "text": "Mora: Let's go!"}
        ],

        "scenes2": [
            {"background": ["Scene1_2Bg0", "Scene1_2Bg1", "Scene1_2Bg2"], "characters": [], "text": "Leon: We finally made it to the forest...", "music": "Scene2.mp3"},
            {"characters": [("Mora", "right", "fadein")], "text": "Mora: It was tough, but we made it..."},
            {"characters": [("Leon", "left", "fadein")], "text": "Leon: I still can't believe what we went through."},
            {"characters": [("Luri", "right", "fadein")], "text": "Luri: I'm glad you made it!"},
            {"characters": [("Leon", "left", "fadein")], "text": "Leon: Luri!? Where have you been?"},
            {"characters": [("Mora", "right", "fadein")], "text": "Mora: We needed you back there!"},
            {"characters": [("Luri_rindo", "right", "fadein")], "text": "Luri: Hehe... I was... busy... with butterflies."},
            {"characters": [("Luri_assustado", "right", "fadein")], "text": "Luri: WAIT... did you hear that?"},
            {"characters": [("Enemy", "left", "fadein")], "text": "??? : Grrrraaahhh..."},
            {"characters": [("Leon_bravo", "left", "fadein")], "text": "Leon: YOU AGAIN?!"},
            {"characters": [("Mora_brava", "right", "fadein")], "text": "Mora: We're not running this time!"},
            {"characters": [("Enemy", "left", "fadein")], "text": "??? : This is the end for you..."},
            {"characters": [("Luri_assustado", "right", "fadein")], "text": "Luri: I... I'll guard the rear!"},
            {"characters": [("Leon_bravo", "left", "fadein")], "text": "Leon: Get ready!"}
        ],

        "scenes3": [
            {"background": ["Scene1_3Bg0", "Scene1_3Bg1", "Scene1_3Bg2", "Scene1_3Bg3"], "characters": [], "text": "Mora: We're almost there...", "music": "Scene3.mp3"},
            {"background": ["Scene1_3_2Bg"], "characters": [("Mora", "left", "fadein"), ("Leon", "right", "fadein")], "text": "Leon: Are you sure it's safe?"},
            {"background": ["Scene1_3_3Bg"], "characters": [("Mora", "left", "fadein")], "text": "Mora: No. But we have no choice."},
            {"background": ["Scene1_3_4Bg"], "characters": [("Mora", "left", "fadein"), ("Luri", "right", "fadein")], "text": "Luri: You finally made it..."},
            {"background": ["Scene1_3_4Bg"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Luri!? Are you okay?"}
        ]


    }
}


def t(key: str):
    lang = SettingsManager.get("language") or "pt"
    data = LANG_DICT.get(lang, LANG_DICT["pt"]).get(key, key)
    return data
