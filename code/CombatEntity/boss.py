import math
import pygame
import random
from code.system.managers.assetmanager import AssetManager
from code.system.config import ENTITY_SHOT_DELAY, ENTITY_SPEED
from code.shots.enemyshot import EnemyShot
from code.CombatEntity.combatentity import CombatEntity

class Boss(CombatEntity):
    def __init__(self, name: str, position: tuple, window):
        super().__init__(name, position)
        self.window = window
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.last_shot_time = pygame.time.get_ticks()

        self.max_health = 1000
        self.last_special_attack = pygame.time.get_ticks()
        self.special_cooldown = 10000  # 10 segundos

        self.direction = 1  # 1 = descendo, -1 = subindo

        # Animação normal
        self.anim_frames = [
            AssetManager.get_image("Boss_1.png"),
            AssetManager.get_image("Boss_2.png"),
            AssetManager.get_image("Boss_3.png"),
        ]
        self.anim_index = 0
        self.anim_timer = 0

        # Animação de tiro
        self.anim_shooting = False
        self.anim_shoot_timer = 0

    def update(self):
        self.move()
        now = pygame.time.get_ticks()

        if self.anim_shooting and now >= self.anim_shoot_timer:
            self.anim_shooting = False

        # Animação idle
        if not self.anim_shooting:
            self.anim_timer += 1
            if self.anim_timer >= 10:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.anim_frames)

        # 🔄 Fase 2 (abaixo de 50% de vida)
        if self.health < self.max_health * 0.5 and not hasattr(self, "phase_2"):
            self.phase_2 = True
            self.shot_delay = 800
            print("🧠 Boss entrou na fase 2!")

        # 🔥 Ataque especial
        if now - self.last_special_attack >= self.special_cooldown:
            self.last_special_attack = now
            self.spawn_minions()

        # 🎯 Tiro aleatório com lógica adaptativa
        if now - self.last_shot_time >= self.shot_delay:
            if random.random() < 0.5:
                self.fire()
                self.anim_shooting = True
                self.anim_shoot_timer = now + 200

                self.shot_delay = random.choice([400, 800, 1200])
            else:
                self.shot_delay = random.randint(600, 1000)

            self.last_shot_time = now

    def fire(self):
        try:
            sound = AssetManager.get_sound("BossShot.mp3")
            sound.set_volume(0.5)
            sound.play()
        except Exception as e:
            print(f"[Erro ao tocar som do Boss] {e}")

        shot = EnemyShot(name=f"{self.name}Shot", position=self.rect.center)
        self.entity_manager.add_entity(shot)

    def spawn_minions(self):
        from code.factory.enemyfactory import EnemyFactory
        for _ in range(2):
            enemy = EnemyFactory.create("Enemy2")
            enemy.rect.centerx = self.rect.centerx - 50
            enemy.rect.centery = random.randint(50, self.window.get_height() - 50)
            self.entity_manager.add_entity(enemy)

    def move(self):
        if not hasattr(self, 'target_pos'):
            self.target_pos = [self.rect.centerx - 100, self.rect.centery]
            self.move_cooldown = 0
        # no move():
        self.rect.centerx += math.sin(pygame.time.get_ticks() * 0.002) * 2
        self.rect.centery += math.sin(pygame.time.get_ticks() * 0.003) * 2

        self.move_cooldown -= 1
        if self.move_cooldown <= 0:
            self.target_pos = [
                random.randint(self.window.get_width() // 2, self.window.get_width() - 60),
                random.randint(30, self.window.get_height() - 30)
            ]
            self.move_cooldown = 60

        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        if abs(dx) > 2:
            self.rect.centerx += int(dx / abs(dx)) * ENTITY_SPEED[self.name]
        if abs(dy) > 2:
            self.rect.centery += int(dy / abs(dy)) * ENTITY_SPEED[self.name]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shot_delay:
            self.last_shot_time = now
            self.anim_shooting = True
            self.anim_shoot_timer = now + 200
            return EnemyShot(name=f"{self.name}Shot", position=self.rect.center)
        return None

    def draw(self, surface):
        frame = self.anim_frames[self.anim_index]
        # Se estiver atirando, aplica uma tremedeira sutil
        offset_x = math.sin(pygame.time.get_ticks() * 0.03) * 3 if self.anim_shooting else 0
        offset_y = math.sin(pygame.time.get_ticks() * 0.04) * 2

        angle = math.sin(pygame.time.get_ticks() * 0.0025) * 4
        rotated = pygame.transform.rotate(frame, angle)
        rect = rotated.get_rect(center=(self.rect.centerx + offset_x, self.rect.centery + offset_y))
        surface.blit(rotated, rect)

