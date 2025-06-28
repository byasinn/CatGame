import random
import pygame
from code.enemy import Enemy
from code.enemyshot import EnemyShot
from code.entity import Entity
from code.player import Player
from code.playershot import PlayerShot
from code.particle import ImpactParticle
class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if ent.name in ["Boss", "BossShot"]:
            if ent.rect.right < 0:
                ent.health = 0
        if isinstance(ent, Enemy):
            if ent.rect.right < 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= pygame.display.get_surface().get_width():
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right < 0:
                ent.health = 0

    @staticmethod
    def verify_collision_entity(ent1, ent2, entity_manager):
        valid_interaction = False

        if ent1.name == "Boss" and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif ent2.name == "Boss" and isinstance(ent1, PlayerShot):
            valid_interaction = True
        elif ent1.name == "BossShot" and isinstance(ent2, Player):
            valid_interaction = True
        elif ent2.name == "BossShot" and isinstance(ent1, Player):
            valid_interaction = True

        elif isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):

                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

                # Sangue ao atingir inimigos
                if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
                    EntityMediator._spawn_blood(entity_manager, ent1.rect.center, count=2)
                elif isinstance(ent2, Enemy) and isinstance(ent1, PlayerShot):
                    EntityMediator._spawn_blood(entity_manager, ent2.rect.center, count=2)

                # Flash de dano nos jogadores
                if isinstance(ent1, Player):
                    ent1.take_damage_flash()
                if isinstance(ent2, Player):
                    ent2.take_damage_flash()

    @staticmethod
    def __give_score(enemy: Entity, entity_list: list[Entity]):
        if enemy.last_dmg == "Player1Shot":
            for ent in entity_list:
                if ent.name == "Player1":
                    ent.score += enemy.score
        elif enemy.last_dmg == "Player2Shot":
            for ent in entity_list:
                if ent.name == "Player2":
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_manager, entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.verify_collision_entity(entity1, entity2, entity_manager)

    @staticmethod
    def verify_health(entity_manager, entity_list: list[Entity]):
        for ent in entity_list[:]:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)

                    # Sangue ao morrer
                    EntityMediator._spawn_blood(entity_manager, ent.rect.center, count=5)

                    # 🔊 Som de morte
                    try:
                        sound = pygame.mixer.Sound(f"./asset/{ent.name}Death.mp3")
                        sound.set_volume(0.6)
                        sound.play()
                    except Exception as e:
                        print(f"[Erro ao tocar som de morte de {ent.name}] {e}")

                elif ent.name == "Boss":
                    EntityMediator.__give_score(ent, entity_list)
                    try:
                        sound = pygame.mixer.Sound("./asset/BossDeath.mp3")
                        sound.set_volume(0.7)
                        sound.play()
                    except Exception as e:
                        print(f"[Erro ao tocar som de morte do Boss] {e}")

                entity_list.remove(ent)

    @staticmethod
    def _spawn_blood(entity_manager, position, count=3):
        from code.particle import ImpactParticle
        for _ in range(count):
            entity_manager.particles_impact.append(
                ImpactParticle(
                    position=position,
                    color=random.choice([(180, 0, 0), (255, 50, 50)])
                )
            )