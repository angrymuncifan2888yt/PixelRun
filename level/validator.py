from pygame import Vector2
from .level import Level
from .entity_factory import ENTITY_FACTORY
from .deserializator import Deserializator
from core import TriggerActivationMode


class Validator:
    @staticmethod
    def is_entity_valid(entity_json: dict) -> bool:
        if not isinstance(entity_json, dict):
            return False

        entity_type = entity_json.get("type")
        if entity_type not in ENTITY_FACTORY:
            return False

        pos = entity_json.get("position")
        if not (
            isinstance(pos, (list, tuple))
            and len(pos) == 2
            and all(isinstance(v, (int, float)) for v in pos)
        ):
            return False

        size = entity_json.get("size")
        if size is not None:
            if not (
                isinstance(size, (list, tuple))
                and len(size) == 2
                and all(isinstance(v, (int, float)) and v > 0 for v in size)
            ):
                return False

        rot = entity_json.get("rotation")
        if rot is not None and not isinstance(rot, (int, float)):
            return False

        color_fill = entity_json.get("color_fill")
        if color_fill is not None:
            if not (
                isinstance(color_fill, (list, tuple))
                and len(color_fill) == 3
                and all(isinstance(c, int) and 0 <= c <= 255 for c in color_fill)
            ):
                return False

        color_border = entity_json.get("color_border")
        if color_border is not None:
            if not (
                isinstance(color_border, (list, tuple))
                and len(color_border) == 3
                and all(isinstance(c, int) and 0 <= c <= 255 for c in color_border)
            ):
                return False

        color = entity_json.get("color")
        if color is not None:
            if not (
                isinstance(color, (list, tuple))
                and len(color) == 3
                and all(isinstance(c, int) and 0 <= c <= 255 for c in color)
            ):
                return False

        opacity = entity_json.get("opacity")
        if opacity is not None:
            if not isinstance(opacity, int) or not (0 <= opacity <= 255):
                return False

        active = entity_json.get("active")
        if active is not None and not isinstance(active, bool):
            return False

        activation_mode = entity_json.get("activation_mode")
        if activation_mode is not None:
            if not isinstance(activation_mode, str):
                return False
            try:
                TriggerActivationMode[activation_mode]
            except KeyError:
                return False

        try:
            from core import World
            temp_world = World()
            entity = Deserializator.load_entity(entity_json, temp_world)
            if entity is None:
                return False
        except Exception:
            return False

        return True

    @staticmethod
    def is_level_valid(level: Level) -> bool:
        if not isinstance(level, Level):
            return False

        if not isinstance(level.player_spawn, Vector2):
            return False

        bg = level.background_color
        if not (
            isinstance(bg, (list, tuple))
            and len(bg) == 3
            and all(isinstance(c, int) and 0 <= c <= 255 for c in bg)
        ):
            return False

        if not isinstance(level.objects, list):
            return False

        for obj in level.objects:
            if not Validator.is_entity_valid(obj):
                return False

        return True
