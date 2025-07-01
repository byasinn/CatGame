import sys
import math
import pygame

from code.DrawableEntity.MovingEntity.background import BackgroundFloat
from code.levels.level1.SceneCinematicSystem import SCENE1_DATA
from code.system.assetmanager import AssetManager
from code.settings.lang import t

# ===============================
# 🔷 SCENES (chamadas pelo level.py)
# ===============================
def run_scene(window):
    clock = pygame.time.Clock()
    font = AssetManager.get_font("VT323-Regular", 22)

    current = 0
    fade_speed = 8
    max_alpha = 255

    while current < len(SCENE1_DATA):
        data = SCENE1_DATA[current]

        bg_list = [BackgroundFloat(bg_name, (0, 0)) for bg_name in data.get("background", [])]

        char_data = data.get("characters", [])
        character_surfs = []
        for name, side, effect in char_data:
            img = AssetManager.get_image(name)
            img.set_alpha(0 if effect == "fadein" else 255)
            rect = img.get_rect()
            if side == "left":
                rect.bottomleft = (- 90, window.get_height() + 60)
            else:
                rect.bottomright = (window.get_width() + 50, window.get_height() + 60)
            character_surfs.append((img, rect, effect))

        text = data.get("text", "")
        lines = wrap_text(text, font, window.get_width() * 0.8)
        fade_alpha = 0
        show_text = False
        skip = False

        while not skip:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and show_text:
                    skip = True

            window.fill((0, 0, 0))

            for bg in bg_list:
                bg.move()
                window.blit(bg.surf, bg.rect)

            for i in range(len(character_surfs)):
                surf, rect, effect = character_surfs[i]
                if effect == "fadein":
                    fade_alpha = min(fade_alpha + fade_speed, max_alpha)
                    surf.set_alpha(fade_alpha)
                elif effect == "slideleft":
                    rect.x -= 1
                window.blit(surf, rect)

            if fade_alpha >= max_alpha or not char_data:
                show_text = True
                for i, line in enumerate(lines):
                    rect = line.get_rect(center=(window.get_width() // 2, window.get_height() - 120 + i * 25))
                    window.blit(line, rect)

            pygame.display.flip()
            clock.tick(60)

        current += 1

    return  # ✅ Sai da função só depois da última cena

def wrap_text(text, font, max_width):
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
                font = AssetManager.get_font("PressStart2P-Regular", 16)
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
