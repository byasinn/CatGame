#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import Surface

from code.core.finishlevel import FinishLevel
from code.levels.arcade.arcade import Arcade
from code.levels.level1.cutscenes1 import run_scene
from code.levels.level1.level1_1 import Level1_0
from code.levels.level1.level1_2 import Level1_2
from code.levels.level1.level1_3 import Level1_3
from code.levels.level2.level2 import Level2
from code.levels.level3.level3 import Level3
from code.core.loadgame import LoadGame

LEVEL_SEQUENCE = ["Level1", "Level1_2", "Level1_3", "Level2", "Level3"]
PHASE_MAP = {
    "Level1": Level1_0,
    "Level1_2": Level1_2,
    "Level1_3": Level1_3,
    "Level2": Level2,
    "Level3": Level3,
}
def get_next_level_name(current_name):
    if current_name in LEVEL_SEQUENCE:
        idx = LEVEL_SEQUENCE.index(current_name)
        if idx + 1 < len(LEVEL_SEQUENCE):
            return LEVEL_SEQUENCE[idx + 1]
    return None

class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int], is_arcade=False, audio=None):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.player_score = player_score
        self.audio = audio
        self.is_arcade = is_arcade

        if self.is_arcade:
            self.logic = Arcade(window, game_mode, player_score, audio)
        else:
            LevelClass = PHASE_MAP.get(name)
            if not LevelClass:
                raise ValueError(f"Fase '{name}' não registrada em PHASE_MAP.")
            self.logic = LevelClass(window, game_mode, player_score, audio)

    def run(self, player_score: list[int]):
        if self.name == "Level1_0":
            if self.audio:
                self.audio.play_music("cutscene1")
            run_scene(self.window)

        result = self.logic.run(player_score)

        if self.name == "Level1_0" and result:
            run_scene(self.window, scene_key="scenes2", count=None)

            next_level = Level(
                self.window,
                "Level1_2",
                self.game_mode,
                player_score,
                self.is_arcade,
                self.audio
            )
            return next_level.run(player_score)

        if result is True:
            LoadGame.save_slot(0, {
                "level": self.name,
                "score": player_score
            })

            finish = FinishLevel(self.window, self.name)
            continuar = finish.run()
            if not continuar:
                return False

            next_level_name = get_next_level_name(self.name)
            if next_level_name:
                next_level = Level(
                    self.window,
                    next_level_name,
                    self.game_mode,
                    player_score,
                    self.is_arcade,
                    self.audio
                )
                return next_level.run(player_score)
            else:
                return False