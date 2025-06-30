import pygame

class AudioController:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.current_music = None

        # 🎵 Músicas de fundo (mp3)
        self.music_tracks = {
            "intro": "./asset/intro.mp3",
            "menu": "./asset/Menu.mp3",
            "level1": "./asset/Level1.mp3",
            "level2": "./asset/Level2.mp3",
            "level3": "./asset/Level3.mp3",
            "arcade": "./asset/LevelArcade.mp3",
            "gameover": "./asset/GameOver.mp3",
            "score": "./asset/Score.mp3",
        }

        # 🔊 Efeitos sonoros (wav ou mp3)
        self.sound_effects = {
            "menu_move": "./asset/MenuMove.wav",
            "menu_select": "./asset/MenuSelect.wav",
            "boss_death": "./asset/BossDeath.mp3",
            "boss_shot": "./asset/BossShot.mp3",
            "enemy1_death": "./asset/Enemy1Death.mp3",
            "enemy2_death": "./asset/Enemy2Death.mp3",
            "enemy1_shot": "./asset/Enemy1Shot.mp3",
            "enemy2_shot": "./asset/Enemy2Shot.mp3",
            "player1_shot": "./asset/Player1Shot.mp3",
            "player2_shot": "./asset/Player2Shot.mp3",
            "aura_burst": "./asset/AuraBurst.mp3",
        }

        # Cache para evitar recarregamento
        self.loaded_sounds = {}

    def play_music(self, name, loop=-1):
        if name == self.current_music:
            return

        path = self.music_tracks.get(name)
        if path:
            try:
                pygame.mixer_music.load(path)
                pygame.mixer_music.set_volume(self.music_volume)
                pygame.mixer_music.play(loop)
                self.current_music = name
            except Exception as e:
                print(f"[Erro ao tocar música '{name}']: {e}")

    def stop_music(self):
        pygame.mixer_music.stop()
        self.current_music = None

    def play_sound(self, name):
        path = self.sound_effects.get(name)
        if not path:
            print(f"[Som não encontrado: {name}]")
            return

        if name not in self.loaded_sounds:
            try:
                self.loaded_sounds[name] = pygame.mixer.Sound(path)
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
