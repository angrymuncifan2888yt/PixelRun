from pygame import Vector2
from .level import Level
from .entity_factory import ENTITY_FACTORY
from .deserializator import Deserializator


class Validator:
    @staticmethod
    def is_entity_valid(entity_json: dict) -> bool:
        if not isinstance(entity_json, dict):
            return False

        # Проверяем обязательное поле type
        entity_type = entity_json.get("type")
        if entity_type not in ENTITY_FACTORY:
            return False

        # Проверка позиции
        pos = entity_json.get("position")
        if not (isinstance(pos, (list, tuple)) and len(pos) == 2 and all(isinstance(v, (int, float)) for v in pos)):
            return False

        # Проверка size если есть
        size = entity_json.get("size")
        if size is not None:
            if not (isinstance(size, (list, tuple)) and len(size) == 2 and all(isinstance(v, (int, float)) and v > 0 for v in size)):
                return False

        # Проверка rotation если есть
        rot = entity_json.get("rotation")
        if rot is not None and not isinstance(rot, (int, float)):
            return False

        # Проверка color если есть
        color = entity_json.get("color")
        if color is not None:
            if not (isinstance(color, (list, tuple)) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color)):
                return False

        # Проверка invisible если есть
        inv = entity_json.get("invisible")
        if inv is not None and not isinstance(inv, bool):
            return False

        # Пробуем создать объект через Deserializator для полной проверки
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

        # Проверка позиции игрока
        if not isinstance(level.player_spawn, Vector2):
            return False

        # Проверка цвета фона
        bg = level.background_color
        if not (isinstance(bg, (list, tuple)) and len(bg) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in bg)):
            return False

        # Проверка объектов
        if not isinstance(level.objects, list):
            return False

        for obj in level.objects:
            if not Validator.is_entity_valid(obj):
                return False

        return True
