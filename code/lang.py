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

        # Cutscene
        "cutscene1_1": "Leon: Miau, parece que vamos ter um dia cheio!",
        "cutscene1_2": "Mora: Cuidado com os inimigos, viu? Eu confio em você ♥",
        "cutscene1_3": "Pressione ENTER para começar!",
        "cutscene2_1": "Mora: Ufa, essa foi difícil!",
        "cutscene2_2": "Leon: A próxima fase vai ser ainda mais intensa, miaaau!",
        "cutscene2_3": "Preparadx? Aperte ENTER!",
        "cutscene3_1": "Leon: É agora, o último desafio!",
        "cutscene3_2": "Mora: Mostre que você é uma verdadeira lenda felina!",
        "cutscene3_3": "Aperte ENTER e brilhe!",
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

        # Cutscene
        "cutscene1_1": "Leon: Meow, looks like we have a busy day ahead!",
        "cutscene1_2": "Mora: Watch out for enemies, okay? I trust you ♥",
        "cutscene1_3": "Press ENTER to start!",
        "cutscene2_1": "Mora: Whew, that was tough!",
        "cutscene2_2": "Leon: Next level will be even more intense, meooow!",
        "cutscene2_3": "Ready? Press ENTER!",
        "cutscene3_1": "Leon: This is it, the final challenge!",
        "cutscene3_2": "Mora: Show them you're a true feline legend!",
        "cutscene3_3": "Press ENTER and shine!",
    }
}

def t(key: str) -> str:
    lang = SettingsManager.get("language") or "pt"
    return LANG_DICT.get(lang, LANG_DICT["pt"]).get(key, key)
