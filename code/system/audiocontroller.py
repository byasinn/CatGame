import os

import pygame

from code.system.assetmanager import AssetManager

class AudioController:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.current_music = None

        self.music_tracks = {
            "intro": "intro.mp3",
            "menu": "Menu.mp3",
            "level1": "Level1.mp3",
            "level2": "Level2.mp3",
            "level3": "Level3.mp3",
            "arcade": "LevelArcade.mp3",
            "gameover": "GameOver.mp3",
            "score": "Score.mp3",
        }

        self.sound_effects = {
            "menu_move": "MenuMove.wav",
            "menu_select": "MenuSelect.wav",
            "boss_death": "BossDeath.mp3",
            "boss_shot": "BossShot.mp3",
            "enemy1_death": "Enemy1Death.mp3",
            "enemy2_death": "Enemy2Death.mp3",
            "enemy1_shot": "Enemy1Shot.mp3",
            "enemy2_shot": "Enemy2Shot.mp3",
            "player1_shot": "Player1Shot.mp3",
            "player2_shot": "Player2Shot.mp3",
            "aura_burst": "AuraBurst.mp3",
        }

        self.loaded_sounds = {}

    def play_music(self, name, loop=-1):
        if name == self.current_music:
            return

        filename = self.music_tracks.get(name)
        if filename:
            try:
                # mesmo sem cache — música geralmente é só uma
                for root, _, files in os.walk(AssetManager.SOUND_DIR):
                    for file in files:
                        if file.lower() == filename.lower():
                            pygame.mixer_music.load(os.path.join(root, file))
                            pygame.mixer_music.set_volume(self.music_volume)
                            pygame.mixer_music.play(loop)
                            self.current_music = name
                            return
            except Exception as e:
                print(f"[Erro ao tocar música '{name}']: {e}")

    def stop_music(self):
        pygame.mixer_music.stop()
        self.current_music = None

    def play_sound(self, name):
        if name not in self.sound_effects:
            print(f"[Som não encontrado: {name}]")
            return

        if name not in self.loaded_sounds:
            try:
                filename = self.sound_effects[name]
                self.loaded_sounds[name] = AssetManager.get_sound(filename)
            except Exception as e:
                print(f"[Erro ao carregar som '{name}']: {e}")
                return

        sound = self.loaded_sounds[name]
        sound.set_volume(self.sfx_volume)
        sound.play()

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        pygame.mixer_music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(1, volume))
        for sound in self.loaded_sounds.values():
            sound.set_volume(self.sfx_volume)

    def get_music_volume(self):
        return self.music_volume

    def get_sfx_volume(self):
        return self.sfx_volume
