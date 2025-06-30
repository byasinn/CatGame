import sys
import math
import pygame
from code.system.assetmanager import AssetManager
from code.settings.lang import t

# ===============================
# 🔷 SCENES (chamadas pelo level.py)
# ===============================
def run_scene(window, scene_name: str, dialogue_count: int = 3):
    """
    Exibe uma cena entre fases (estilo novela com falas traduzidas).
    """
    leon = AssetManager.get_image(f"LeonMenu{scene_name[-1]}.png")
    mora = AssetManager.get_image(f"MoraMenu{scene_name[-1]}.png")
    leon_rect = leon.get_rect(bottomleft=(50, window.get_height() - 30))
    mora_rect = mora.get_rect(bottomright=(window.get_width() - 50, window.get_height() - 30))

    font = AssetManager.get_font("VT323-Regular.ttf", 22)
    dialogues = t(scene_name)
    if not isinstance(dialogues, list):
        dialogues = [dialogues]

    current = 0
    clock = pygame.time.Clock()

    while True:
        window.fill((0, 0, 0))
        window.blit(leon, leon_rect)
        window.blit(mora, mora_rect)

        text = font.render(dialogues[current], True, (255, 255, 255))
        text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
        window.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if current < len(dialogues) - 1:
                    current += 1
                else:
                    return

        clock.tick(60)

# ===============================
# 🔶 CUTSCENES (dentro de levels, com NPCs)
# ===============================
class CutsceneManager:
    def __init__(self, window, player):
        self.window = window
        self.player = player
        self.done = False
        self.phase = 0

        self.dialogue_list = [
            ("npc", "Que bom que você já chegou, eles estão por toda parte!"),
            ("player", "Onde? Quem?"),
            ("npc", "Fique atento, não confie em ninguém!"),
        ]
        self.npc_img = AssetManager.get_image("NpcSprite.png")
        self.npc_pos_x = window.get_width() + 100
        self.npc_target_x = window.get_width() // 2 + 80

    def update(self, event_list):
        # NPC se move da direita até o centro
        if self.npc_pos_x > self.npc_target_x:
            self.npc_pos_x -= 6

        npc_y = self.window.get_height() // 2 + math.sin(pygame.time.get_ticks() * 0.005) * 8
        npc_rect = self.npc_img.get_rect(center=(self.npc_pos_x, npc_y))
        self.window.blit(self.npc_img, npc_rect)

        if self.npc_pos_x <= self.npc_target_x:
            if self.phase < len(self.dialogue_list):
                speaker, message = self.dialogue_list[self.phase]
                font = pygame.font.Font("./asset/PressStart2P-Regular.ttf", 14)
                wrapped_lines = self.render_wrapped_text(message, font, self.window.get_width() // 2.5)

                base_pos = (
                    npc_rect.centerx if speaker == "npc" else self.player.rect.centerx,
                    npc_rect.top - 30 if speaker == "npc" else self.player.rect.top - 30
                )

                for i, line in enumerate(wrapped_lines):
                    rect = line.get_rect(center=(base_pos[0], base_pos[1] + i * 18))
                    self.window.blit(line, rect)

                for event in event_list:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.phase += 1
            else:
                self.done = True

    def render_wrapped_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = current + word + " "
            if font.size(test)[0] < max_width:
                current = test
            else:
                lines.append(font.render(current.strip(), True, (255, 255, 255)))
                current = word + " "
        if current:
            lines.append(font.render(current.strip(), True, (255, 255, 255)))
        return lines
