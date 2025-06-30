#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import sys
from pygame import Surface
from code.system.assetmanager import AssetManager
from code.settings.lang import t


def run_scene(window: Surface, scene_name: str, dialogue_count: int = 3):
    """
    Exibe uma cutscene com base em um identificador e número de falas.
    :param window: janela do jogo
    :param scene_name: nome base das falas no dicionário (ex: "cutscene1")
    :param dialogue_count: número de falas que a cena terá
    """

    # Imagens dos personagens
    leon = AssetManager.get_image(f"LeonMenu{scene_name[-1]}.png")
    mora = AssetManager.get_image(f"MoraMenu{scene_name[-1]}.png")
    leon_rect = leon.get_rect(bottomleft=(50, window.get_height() - 30))
    mora_rect = mora.get_rect(bottomright=(window.get_width() - 50, window.get_height() - 30))

    # Fonte
    font = AssetManager.get_font("VT323-Regular.ttf", 22)

    # Diálogos
    dialogues = [t(f"{scene_name}_{i + 1}") for i in range(dialogue_count)]

    current = 0
    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        window.blit(leon, leon_rect)
        window.blit(mora, mora_rect)

        text = font.render(dialogues[current], True, (255, 255, 255))
        text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
        window.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if current < len(dialogues) - 1:
                    current += 1
                else:
                    return

        clock.tick(60)
