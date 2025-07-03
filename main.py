import os
import pygame
from code.core.game import Game

icon_path = os.path.join("asset", "icon.ico")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

game = Game()
game.run()

