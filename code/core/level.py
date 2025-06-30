#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import Surface

# Importa as fases da campanha
from code.core.levels.level1 import Level1
from code.core.levels.level2 import Level2
from code.core.levels.level3 import Level3

# Mapeia os nomes usados no game.py para suas classes
PHASE_MAP = {
    "Level1": Level1,
    "Level2": Level2,
    "Level3": Level3,
    # Se quiser adicionar depois:
    # "Level1_1": Level1_1,
    # "Level2_1": Level2_1,
}

class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int], is_arcade=False, audio=None):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.player_score = player_score
        self.audio = audio
        self.is_arcade = is_arcade



        if self.is_arcade:
            # Aqui você pode criar um LevelArcade separado futuramente
            from code.core.levels.level1 import Level1  # Temporário para testes no arcade
            self.logic = Level1(window, game_mode, player_score, audio)
        else:
            LevelClass = PHASE_MAP.get(name)
            if not LevelClass:
                raise ValueError(f"Fase '{name}' não registrada em PHASE_MAP.")
            self.logic = LevelClass(window, game_mode, player_score, audio)

    def run(self, player_score: list[int]):
        return self.logic.run(player_score)
