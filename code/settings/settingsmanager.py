import json
import os

class SettingsManager:
    DEFAULTS = {
        "resolution_index": 2,
        "fullscreen": False,
        "music_volume": 0.6,
        "sfx_volume": 0.8,
        "language": "pt",
        "visual_effects": True,
        "gore": True,
    }

    _settings = DEFAULTS.copy()
    _path = "./settings.json"


    @classmethod
    def load(cls):
        if os.path.exists(cls._path):
            try:
                with open(cls._path, "r") as f:
                    data = json.load(f)
                    for key, default in cls.DEFAULTS.items():
                        cls._settings[key] = data.get(key, default)
            except Exception:
                pass

    @classmethod
    def save(cls):
        with open(cls._path, "w") as f:
            json.dump(cls._settings, f, indent=2)

    @classmethod
    def get(cls, key):
        return cls._settings.get(key, cls.DEFAULTS.get(key))

    @classmethod
    def set(cls, key, value):
        cls._settings[key] = value
        cls.save()

