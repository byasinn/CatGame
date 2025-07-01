import pygame
from code.factory.entityFactory import EntityFactory

class TutorialManager:
    def __init__(self, entity_manager, window, player):
        self.window = window
        self.entity_manager = entity_manager
        self.player = player

        self.step = 0
        self.done = False
        self.enemy_spawned = False
        self.last_shot_state = False

    def update(self):
        keys = pygame.key.get_pressed()

        just_shot = self.player.shot_fired and not self.last_shot_state
        self.last_shot_state = self.player.shot_fired  # atualiza o estado
        shot = self.player.shoot()
        if shot:
            self.entity_manager.add_entity(shot)

        if self.step == 0:
            self.draw_text("Mova-se com as setas ou WASD")
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
                self.step += 1

        elif self.step == 1:
            self.draw_text("Atire com Ctrl")
            if just_shot:
                self.step += 1

        elif self.step == 2:
            self.draw_text("Derrote o inimigo!")
            if not self.enemy_spawned:
                enemy = EntityFactory.get_entity("EnemyTest", window=self.window)
                enemy.hp = 1
                enemy.frozen = False
                self.entity_manager.add_entity(enemy)
                self.enemy_spawned = True
            if not any(e.name == "EnemyTest" for e in self.entity_manager.get_entities()):
                self.step += 1

        elif self.step == 3:
            self.draw_text("Parabéns! Prepare-se...", darken=False)
            self.done = True

    def draw_text(self, message: str, darken=False, blink=False):
        from code.core.hud import HUDRenderer
        HUDRenderer(self.window).draw_tutorial_message(self.window, message, darken=darken, blink=blink)
