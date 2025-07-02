#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import Surface
# Importa a cena 1 formatada com SCENE1_DATA
from code.levels.level1.cutscenes1 import run_scene
from code.levels.level1.level1_1 import Level1_0
from code.levels.level1.level1_2 import Level1_2
from code.levels.level2.level2 import Level2
from code.levels.level3.level3 import Level3


# Mapeia os nomes usados no game.py para suas classes
PHASE_MAP = {
    "Level1": Level1_0,
    "Level1_2": Level1_2,
    "Level2": Level2,
    "Level3": Level3,
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
            from code.levels import Level1  # Temporário para testes no arcade
            self.logic = Level1(window, game_mode, player_score, audio)
        else:
            LevelClass = PHASE_MAP.get(name)
            if not LevelClass:
                raise ValueError(f"Fase '{name}' não registrada em PHASE_MAP.")
            self.logic = LevelClass(window, game_mode, player_score, audio)

    def run(self, player_score: list[int]):
        # CENA DE ABERTURA da campanha (antes de Level1)
        if self.name == "Level1":
            if self.audio:
                self.audio.play_music("cutscene1")
            run_scene(self.window)



        # ✅ Inicia o Level correspondente (ex: Level1_0)
        result = self.logic.run(player_score)

        # Transição de Level1 → cutscene2 → Level1_2
        if self.name == "Level1" and result:
            run_scene(self.window, scene_key="scenes2", count=None)



            # Cria o próximo Level e executa
            next_level = Level(
                self.window,
                "Level1_2",
                self.game_mode,
                player_score,
                self.is_arcade,
                self.audio
            )
            return next_level.run(player_score)

        return result

