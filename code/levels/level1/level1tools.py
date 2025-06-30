from code.system.assetmanager import AssetManager
from code.settings.settingsmanager import SettingsManager

def setup_visual_effects(entity_manager):
    """Ativa ou desativa efeitos visuais conforme as configurações do jogador."""
    effects_enabled = SettingsManager.get("visual_effects")
    entity_manager.enable_ambient_particles = effects_enabled
    entity_manager.enable_magic_fog = effects_enabled

def get_level_overlay_image():
    """Carrega a imagem de luz sobreposta da fase."""
    return AssetManager.get_image("LightOverlay_Level1.png")

def load_background_entities():
    """Carrega entidades de fundo para o Level1."""
    from code.factory.entityFactory import EntityFactory
    return EntityFactory.get_entity("Level1Bg")
