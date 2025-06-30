from code.CombatEntity.player import Player
from code.shots.playershot import PlayerShot
from code.CombatEntity.enemy import Enemy
from code.shots.enemyshot import EnemyShot
from code.CombatEntity.boss import Boss
from code.system.particle import ImpactParticle, AuraBurstParticle

class CollisionMap:
    RULES = {}

    @staticmethod
    def register(type1, type2):
        def decorator(func):
            CollisionMap.RULES[(type1, type2)] = func
            return func
        return decorator

    @staticmethod
    def handle_collision(ent1, ent2, entity_manager):
        rects_collide = (
            ent1.rect.right >= ent2.rect.left and
            ent1.rect.left <= ent2.rect.right and
            ent1.rect.bottom >= ent2.rect.top and
            ent1.rect.top <= ent2.rect.bottom
        )

        if not rects_collide:
            return False

        key = (type(ent1), type(ent2))
        reverse = (type(ent2), type(ent1))

        if key in CollisionMap.RULES:
            return CollisionMap.RULES[key](ent1, ent2, entity_manager)
        elif reverse in CollisionMap.RULES:
            return CollisionMap.RULES[reverse](ent2, ent1, entity_manager)

        return False

@CollisionMap.register(PlayerShot, Enemy)
def handle_player_shot_hits_enemy(shot, enemy, manager):
    enemy.health -= shot.damage
    shot.health -= enemy.damage
    enemy.last_dmg = shot.name

    manager.particles_impact.append(ImpactParticle(enemy.rect.center))
    return True


@CollisionMap.register(PlayerShot, Boss)
def handle_player_shot_hits_boss(shot, boss, manager):
    boss.health -= shot.damage
    shot.health -= boss.damage
    boss.last_dmg = shot.name
    manager.particles_impact.append(ImpactParticle(boss.rect.center, color=(255, 200, 0)))
    return True


@CollisionMap.register(EnemyShot, Player)
def handle_enemy_shot_hits_player(shot, player, manager):
    player.health -= shot.damage
    shot.health -= player.damage
    player.last_dmg = shot.name

    player.take_damage_flash()
    player.damage_counter += 1
    player.damage_timer = 30

    if player.damage_counter >= 3:
        manager.particles_impact.append(AuraBurstParticle(player.rect.center))
        player.damage_counter = 0

    return True
