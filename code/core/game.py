#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.settings.display import apply_resolution
from code.core.menu import Menu
from code.system.controllers.audiocontroller import AudioController
from code.system.introscreen import show_intro_text, show_second_intro_screen, show_intro_screen

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.window = apply_resolution()
        if not self.window:
            raise RuntimeError("Erro ao aplicar resolução. A janela não foi criada.")

        self.audio = AudioController()

    def run(self):
        show_intro_screen(self.window, self.audio)
        show_second_intro_screen(self.window)

        # O controle é delegado ao Menu
        menu = Menu(self.window, self.audio)
        menu.run_loop()