import json
from .const import SAVE_FILE_FILE_PATH
from .skins import Skins


class PlayerData:
    @classmethod
    def save(cls):
        data = {
            "settings": {
                "editor_camera_speed": cls.EDITOR_CAMERA_SPEED,
                "target_fps": cls.TARGET_FPS,
                "window_background_color": list(cls.WINDOW_BACKGROUND_COLOR),
                "world_load_distance": cls.WORLD_LOAD_DISTANCE,
                "music_volume": cls.MUSIC_VOLUME,
                "player_volume": cls.PLAYER_VOLUME,
                "player_death_volume": cls.PLAYER_DEATH_VOLUME,
                "camera_speed": cls.CAMERA_SPEED,
                "cube_skin": cls.CUBE_SKIN.name,
                "ufo_skin": cls.UFO_SKIN.name
            }
        }

        try:
            with open(SAVE_FILE_FILE_PATH, "w") as file:
                json.dump(data, file)
        except Exception:
            pass

    @classmethod
    def init(cls):
        cls.EDITOR_CAMERA_SPEED = 2000
        cls.TARGET_FPS = 120
        cls.WINDOW_BACKGROUND_COLOR = (25, 25, 25)
        cls.WORLD_LOAD_DISTANCE = 1200
        cls.MUSIC_VOLUME = 0.5
        cls.CAMERA_SPEED = 6.0

        cls.PLAYER_VOLUME = 1
        cls.PLAYER_DEATH_VOLUME = 1

        cls.CUBE_SKIN = Skins.CUBE_SKINS[0]
        cls.UFO_SKIN = Skins.UFO_SKINS[0] if Skins.UFO_SKINS else cls.CUBE_SKIN

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

        cls.MUSIC_VOLUME = cls._safe_float(
            settings.get("music_volume"),
            cls.MUSIC_VOLUME
        )

        cls.PLAYER_VOLUME = cls._safe_float(
            settings.get("player_volume"),
            cls.PLAYER_VOLUME
        )

        cls.PLAYER_DEATH_VOLUME = cls._safe_float(
            settings.get("player_death_volume"),
            cls.PLAYER_DEATH_VOLUME
        )

        cls.CAMERA_SPEED = cls._safe_float(
            settings.get("camera_speed"),
            cls.CAMERA_SPEED
        )

        cube_skin_name = settings.get("cube_skin", cls.CUBE_SKIN.name)
        ufo_skin_name = settings.get("ufo_skin", cls.UFO_SKIN.name)

        cls.CUBE_SKIN = next(
            (skin for skin in Skins.ALL_SKINS if skin.name == cube_skin_name),
            Skins.CUBE_SKINS[0]
        )

        cls.UFO_SKIN = next(
            (skin for skin in Skins.ALL_SKINS if skin.name == ufo_skin_name),
            Skins.UFO_SKINS[0] if Skins.UFO_SKINS else cls.CUBE_SKIN
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