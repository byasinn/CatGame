#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.const import WIN_HEIGHT, COLOR_WHITE, MENU_OPTION, EVENT_ENEMY, EVENT_TIMEOUT, SPAWN_TIME, TIMEOUT_STEP, \
    TIMEOUT_LEVEL
from code.enemy import Enemy
from code.player import Player
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.entitymediator import EntityMediator


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.window = window
        self.timeout = TIMEOUT_LEVEL
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + "Bg"))
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)
        if game_mode in [MENU_OPTION[1],MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        self.boss_summoned = False
        self.boss_delay = 5000  # 5 segundos em ms
        self.boss_timer = 0
        self.boss_kill_trigger = 10  # após matar 10 entidades
        self.kills = 0


        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)


    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.boss_timer += clock.get_time()

            if not self.boss_summoned and self.name == 'Level3':
                if self.boss_timer > self.boss_delay or self.kills >= self.boss_kill_trigger:
                    self.entity_list.append(EntityFactory.get_entity("Boss"))
                    self.boss_summoned = True
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
                    angle = math.sin(pygame.time.get_ticks() * 0.002) * 5

                    surf = pygame.transform.rotate(ent.surf, angle)

                    rect = surf.get_rect(center=(ent.rect.centerx, ent.rect.centery + offset))
                    self.window.blit(surf, rect)
                else:
                    self.window.blit(ent.surf, ent.rect)

                ent.move()
                if isinstance(ent, (Player, Enemy)) or ent.name == "Boss":
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)
                if ent.name == "Player1":
                    self.level_text(14, f'Mora - Health: {ent.health} | Score: {ent.score}', COLOR_WHITE, (10, 25))
                if ent.name == "Player2":
                    self.level_text(14, f'Leon - Health: {ent.health} | Score: {ent.score}', COLOR_WHITE, (10, 45))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', "Enemy2"))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, (Player, Entity)):
                        found_player = True
                if not found_player:
                    return False

            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000 : .1f}s', COLOR_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps() :.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(24, f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()
            # Collision
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

            for ent in self.entity_list:
                if isinstance(ent, Enemy) and ent.health <= 0:
                    self.kills += 1
    pass

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)