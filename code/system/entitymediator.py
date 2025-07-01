import random
import pygame
from code.CombatEntity.enemy import Enemy
from code.system.assetmanager import AssetManager
from code.system.collisionmap import CollisionMap
from code.shots.enemyshot import EnemyShot
from code.system.entity import Entity
from code.shots.playershot import PlayerShot
from code.settings.settingsmanager import SettingsManager


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
        CollisionMap.handle_collision(ent1, ent2, entity_manager)

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
                    if ent.name == "Boss":
                        EntityMediator.__give_score(ent, entity_list)
                        try:
                            sound = AssetManager.get_sound("BossDeath.mp3")
                            sound.set_volume(0.7)
                            sound.play()
                        except Exception as e:
                            print(f"[Erro ao tocar som de morte do Boss] {e}")

                    else:
                        try:
                            sound = AssetManager.get_sound(f"{ent.name}Death.mp3")
                            sound.set_volume(0.6)
                            sound.play()
                        except Exception as e:
                            print(f"[Erro ao tocar som de morte de {ent.name}] {e}")

                entity_list.remove(ent)

    @staticmethod
    def _spawn_blood(entity_manager, position, count=3):
        from code.system.particle import ImpactParticle

        if not SettingsManager.get("gore"):
            return

        for _ in range(count):
            entity_manager.particles_impact.append(
                ImpactParticle(
                    position=position,
                    color=random.choice([(180, 0, 0), (255, 50, 50)])
                )
            )