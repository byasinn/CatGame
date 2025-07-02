from code.factory.playerfactory import PlayerFactory
from code.factory.enemyfactory import EnemyFactory
from code.factory.backgroundfactory import BackgroundFactory

class EntityFactory:
    @staticmethod
    def get_entity(name: str, window=None):
        if name in ["Player1", "Player2"]:
            return PlayerFactory.create(name)

        elif name in ["Enemy1", "Enemy2", "Boss"]:
            return EnemyFactory.create(name)

        elif name.endswith("Bg"):
            return BackgroundFactory.create(name[:-2])

        elif name == "EnemyTest":
            from code.CombatEntity.enemy import Enemy
            enemy = Enemy("EnemyTest", position=(300, 200), window=window)
            enemy.hp = 1
            return enemy

        else:
            raise ValueError(f"Entidade desconhecida: {name}")


