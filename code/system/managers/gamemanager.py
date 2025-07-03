from code.levels.level import Level

class GameManager:
    def __init__(self, window, audio):
        self.window = window
        self.audio = audio

    def start_campaign(self, mode: str) -> bool:
        """
        Inicia a campanha a partir do Level1, com cutscene.
        """
        player_score = [0, 0]
        level = Level(self.window, 'Level1', mode, player_score, is_arcade=False, audio=self.audio)
        result = level.run(player_score)
        if not result:
            from code.core.gameover import GameOver
            GameOver(self.window).show()
        return result

    def start_arcade(self, mode: str) -> bool:
        """
        Inicia o modo arcade. (A lógica ainda será expandida)
        """
        from code.levels.arcade.arcade import Arcade  # ← Você criará esse arquivo depois
        player_score = [0, 0]
        arcade = Arcade(self.window, mode, player_score, self.audio)
        return arcade.run(player_score)

    def load_game(self):
        """
        Placeholder: lógica de carregar jogo salvo ainda será implementada
        """
        print("[LOAD GAME ainda não implementado]")
        return False