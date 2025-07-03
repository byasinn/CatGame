import os
import json
import sys
import pygame
from code.settings.lang import t
from code.system.config import COLOR_WHITE, COLOR_YELLOW, COLOR_PINK
from code.system.keys import MENU_KEYS
from code.system.managers.assetmanager import AssetManager
from code.system.particle import draw_grain_overlay

SAVE_FOLDER = "saves"
os.makedirs(SAVE_FOLDER, exist_ok=True)

class LoadGame:
    MAX_SLOTS = 3

    @staticmethod
    def _get_file_path(slot_index: int):
        return os.path.join(SAVE_FOLDER, f"slot{slot_index}.json")

    @staticmethod
    def save_slot(slot_index: int, data: dict):
        path = LoadGame._get_file_path(slot_index)
        with open(path, "w") as file:
            json.dump(data, file)

    @staticmethod
    def load_slot(slot_index: int) -> dict:
        path = LoadGame._get_file_path(slot_index)
        if os.path.exists(path):
            with open(path, "r") as file:
                return json.load(file)
        return {}

    @staticmethod
    def clear_slot(slot_index: int):
        path = LoadGame._get_file_path(slot_index)
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def get_all_slots() -> list:
        return [
            LoadGame.load_slot(i)
            for i in range(LoadGame.MAX_SLOTS)
        ]

    @staticmethod
    def run_load_game(window, audio):
        slots = LoadGame.get_all_slots()
        selected = 0
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            window.fill((0, 0, 0))
            width, height = window.get_size()

            font = AssetManager.get_font("VT323-Regular.ttf", 30)
            title = font.render(t("load_game_title"), True, COLOR_PINK)
            window.blit(title, title.get_rect(center=(width // 2, int(height * 0.1))))

            for i, slot in enumerate(slots):
                if "level" in slot:
                    label = f"Slot {i + 1}: {slot['level']} - Score: {slot['score'][0]}"
                else:
                    label = f"Slot {i + 1}: {t('empty_slot')}"
                color = COLOR_YELLOW if i == selected else COLOR_WHITE
                font = AssetManager.get_font("VT323-Regular.ttf", 22)
                rendered = font.render(label, True, color)
                window.blit(rendered, rendered.get_rect(center=(width // 2, int(height * 0.3 + i * 80))))

            font = AssetManager.get_font("VT323-Regular.ttf", 16)
            msg = font.render(t("press_esc_menu"), True, COLOR_WHITE)
            window.blit(msg, msg.get_rect(center=(width // 2, int(height * 0.85))))

            draw_grain_overlay(window)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in MENU_KEYS["up"]:
                        selected = (selected - 1) % len(slots)
                        audio.play_sound("menu_move")
                    elif event.key in MENU_KEYS["down"]:
                        selected = (selected + 1) % len(slots)
                        audio.play_sound("menu_move")
                    elif event.key in MENU_KEYS["select"]:
                        if "level" in slots[selected]:
                            from code.levels.level import Level
                            level = Level(window, slots[selected]["level"], "solo", slots[selected]["score"],audio=audio)
                            return level.run(slots[selected]["score"])
                        else:
                            audio.play_sound("error")
                    elif event.key in MENU_KEYS["back"]:
                        return
