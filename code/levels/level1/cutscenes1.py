import random
import sys
import math
import pygame
from code.DrawableEntity.MovingEntity.background import BackgroundFloat
from code.levels.level1.SceneCinematicSystem import SCENE1_DATA, SCENE2_DATA, SCENE3_DATA
from code.system.managers.assetmanager import AssetManager

# 🔷 SCENES (chamadas pelo level.py)
SCENE_DATASETS = {
    "scenes1": SCENE1_DATA,
    "scenes2": SCENE2_DATA,
    "scenes3": SCENE3_DATA,
}

def run_scene(window, scene_key="scenes1", count=None):
    clock = pygame.time.Clock()
    font = AssetManager.get_font("VT323-Regular", 22)

    type_sound = AssetManager.get_sound("Type1.mp3")
    next_sound = AssetManager.get_sound("DialogueAdvance.mp3")

    scene_data = SCENE_DATASETS.get(scene_key)
    if not scene_data:
        print(f"[Cena '{scene_key}' não encontrada]")
        return

    current = 0
    fade_speed = 8
    max_alpha = 255
    scene_number = scene_key[-1]  # para usar no nome do arquivo da imagem

    while current < (count if count is not None else len(scene_data)):
        data = scene_data[current]
        text = data.get("text", "")
        text_chars = list(text)

        if current == 0 or ("background" in data and data["background"]):
            bg_list = [BackgroundFloat(bg_name, (0, 0)) for bg_name in data.get("background", [])]

        char_data = data.get("characters", [])
        character_surfs = []
        for name, side, effect in char_data:
            filename = f"{name}Scene{scene_number}.png"
            img = AssetManager.get_image(filename)
            img.set_alpha(0 if effect == "fadein" else 255)
            rect = img.get_rect()
            if side == "left":
                rect.bottomleft = (-90, window.get_height() + 60)
            else:
                rect.bottomright = (window.get_width() + 50, window.get_height() + 60)
            character_surfs.append((img, rect, effect))

        typed_text = ""
        char_index = 0
        typing_delay = 2
        typing_timer = 0
        text_done = False
        fade_alpha = 0
        skip = False

        while not skip:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and text_done:
                    next_sound.play()
                    skip = True

            window.fill((0, 0, 0))

            for bg in bg_list:
                bg.move()
                window.blit(bg.surf, bg.rect)

            for i, (surf, rect, effect) in enumerate(character_surfs):
                if effect == "fadein":
                    fade_alpha = min(fade_alpha + fade_speed, max_alpha)
                    surf.set_alpha(fade_alpha)
                elif effect == "slideleft":
                    rect.x -= 1
                window.blit(surf, rect)

            if fade_alpha >= max_alpha or not char_data:
                if not text_done and typing_timer == 0 and char_index < len(text_chars):
                    typed_text += text_chars[char_index]
                    char_index += 1
                    typing_timer = typing_delay
                    type_sound.set_volume(random.uniform(0.10, 0.20))
                    type_sound.play()
                elif char_index >= len(text_chars):
                    text_done = True

                if typing_timer > 0:
                    typing_timer -= 1

                rendered_text = font.render(typed_text, True, (255, 255, 255))
                rect = rendered_text.get_rect(center=(window.get_width() // 2, window.get_height() - 100))
                window.blit(rendered_text, rect)

            pygame.display.flip()
            clock.tick(60)

        current += 1

# CUTSCENES (dentro de levels, com NPCs)
class CutsceneManager:
    SCALE_FACTOR = 0.50
    NPC_SPEED = 6
    ANIM_DELAY = 10
    FONT_NAME = "PressStart2P-Regular"
    FONT_SIZE = 16
    LINE_SPACING = 18

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

        original_frames = [
            AssetManager.get_image("LuriSprite1.png"),
            AssetManager.get_image("LuriSprite2.png"),
            AssetManager.get_image("LuriSprite3.png")
        ]

        self.npc_frames = [
            pygame.transform.smoothscale(frame, (
                int(frame.get_width() * self.SCALE_FACTOR),
                int(frame.get_height() * self.SCALE_FACTOR)
            )) for frame in original_frames
        ]

        self.npc_anim_index = 0
        self.npc_anim_timer = 0
        self.npc_pos_x = window.get_width() + 100
        self.npc_target_x = window.get_width() // 2 + 80

    def update_npc_animation(self):
        self.npc_anim_timer += 1
        if self.npc_anim_timer >= self.ANIM_DELAY:
            self.npc_anim_timer = 0
            self.npc_anim_index = (self.npc_anim_index + 1) % len(self.npc_frames)

    def render_npc(self):
        npc_y = self.window.get_height() // 2 + math.sin(pygame.time.get_ticks() * 0.005) * 8
        npc_img = self.npc_frames[self.npc_anim_index]
        npc_rect = npc_img.get_rect(center=(self.npc_pos_x, npc_y))
        self.window.blit(npc_img, npc_rect)
        return npc_rect

    def update(self, event_list):
        if self.npc_pos_x > self.npc_target_x:
            self.npc_pos_x -= self.NPC_SPEED
            self.update_npc_animation()
            self.render_npc()
            return

        self.update_npc_animation()
        npc_rect = self.render_npc()

        if self.phase >= len(self.dialogue_list):
            self.done = True
            return

        speaker, message = self.dialogue_list[self.phase]
        font = AssetManager.get_font(self.FONT_NAME, self.FONT_SIZE)
        wrapped_lines = self.render_wrapped_text(message, font, self.window.get_width() // 2.5)

        base_x = npc_rect.centerx if speaker == "npc" else self.player.rect.centerx
        base_y = npc_rect.top - 30 if speaker == "npc" else self.player.rect.top - 30

        for i, line in enumerate(wrapped_lines):
            rect = line.get_rect(center=(base_x, base_y + i * self.LINE_SPACING))
            self.window.blit(line, rect)

        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.phase += 1

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