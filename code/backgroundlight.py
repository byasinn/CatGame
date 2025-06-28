from code.entity import Entity

class BackgroundLight(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        pass  # luz não se move
