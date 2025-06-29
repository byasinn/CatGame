from code.factory.playerfactory import PlayerFactory
from code.factory.enemyfactory import EnemyFactory
from code.factory.backgroundfactory import BackgroundFactory

class EntityFactory:
    @staticmethod
    def get_entity(name: str):
        if name in ["Player1", "Player2"]:
            return PlayerFactory.create(name)
        elif name in ["Enemy1", "Enemy2", "Boss"]:
            return EnemyFactory.create(name)
        elif "Bg" in name:
            base = name.replace("Bg", "")
            return BackgroundFactory.create(base)
        else:
            raise ValueError(f"Entidade desconhecida: {name}")
