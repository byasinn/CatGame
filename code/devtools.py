import pygame
from code.levels.level import Level
from code.core.gameover import GameOver

def handle_dev_keys(event, window, audio):
    """
    Atalhos secretos de desenvolvedor.
    Ativado a partir do menu, durante o loop principal.
    Pressione:
      1 → Level1 (campanha solo)
      2 → Level1_2 (arcade solo)
      3 → Level1 (campanha cooperativo)
    """

    if event.type != pygame.KEYDOWN:
        return False

    player_score = [0, 0]

    # Fase 1: Campanha Solo
    if event.key == pygame.K_1:
        level = Level(window, "Level1", "solo", player_score, is_arcade=False, audio=audio)
        result = level.run(player_score)
        if not result:
            GameOver(window).show()
        return True

    # Fase 2: Arcade Solo
    elif event.key == pygame.K_2:
        level = Level(window, "Level1_2", "solo", player_score, is_arcade=True, audio=audio)
        result = level.run(player_score)
        if not result:
            GameOver(window).show()
        return True

    # Fase 3: Campanha Cooperativa
    elif event.key == pygame.K_3:
        level = Level(window, "Level1_3", "solo", player_score, is_arcade=False, audio=audio)
        result = level.run(player_score)
        if not result:
            GameOver(window).show()
        return True

    return False
