import json
from .const import SAVE_FILE_FILE_PATH


class PlayerData:
    EDITOR_CAMERA_SPEED = 2000
    TARGET_FPS = 120
    WINDOW_BACKGROUND_COLOR = (25, 25, 25)
    WORLD_LOAD_DISTANCE = 1200
    BACKGROUND_MUSIC_VOLUME = 0.5

    @classmethod
    def save(cls):
        data = {
            "settings": {
                "editor_camera_speed": cls.EDITOR_CAMERA_SPEED,
                "target_fps": cls.TARGET_FPS,
                "window_background_color": list(cls.WINDOW_BACKGROUND_COLOR),
                "world_load_distance": cls.WORLD_LOAD_DISTANCE,
                "background_music_volume": cls.BACKGROUND_MUSIC_VOLUME
            }
        }

        try:
            with open(SAVE_FILE_FILE_PATH, "w") as file:
                json.dump(data, file, indent=4)
        except Exception:
            pass

    @classmethod
    def init(cls):
        try:
            with open(SAVE_FILE_FILE_PATH, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        settings = data.get("settings", {})

        cls.EDITOR_CAMERA_SPEED = cls._safe_float(
            settings.get("editor_camera_speed"),
            cls.EDITOR_CAMERA_SPEED
        )

        cls.TARGET_FPS = cls._safe_int(
            settings.get("target_fps"),
            cls.TARGET_FPS
        )

        cls.WINDOW_BACKGROUND_COLOR = cls._safe_color(
            settings.get("window_background_color"),
            cls.WINDOW_BACKGROUND_COLOR
        )

        cls.WORLD_LOAD_DISTANCE = cls._safe_int(
            settings.get("world_load_distance"),
            cls.WORLD_LOAD_DISTANCE
        )

        cls.BACKGROUND_MUSIC_VOLUME = cls._safe_float(
            settings.get("background_music_volume"),
            cls.BACKGROUND_MUSIC_VOLUME
        )

    @staticmethod
    def _safe_int(value, default):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_float(value, default):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_color(value, default):
        try:
            if isinstance(value, (list, tuple)) and len(value) == 3:
                return tuple(int(v) for v in value)
        except Exception:
            pass
        return default