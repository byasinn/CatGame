from code.system.managers.assetmanager import AssetManager
from code.system.entity import Entity

class DrawableEntity(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.image = AssetManager.get_image(f"{name}.png")
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
