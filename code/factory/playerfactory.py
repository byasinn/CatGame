from code.CombatEntity.player import Player
import pygame

class PlayerFactory:
    @staticmethod
    def create(player_id: str):
        surface = pygame.display.get_surface()
        y = surface.get_height() / 2 - 30 if player_id == "Player1" else surface.get_height() / 2 + 30
        return Player(player_id, (10, y), surface)
