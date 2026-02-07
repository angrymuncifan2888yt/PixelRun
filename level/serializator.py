from .level import Level
from core import Entity
from .entity_factory import ENTITY_FACTORY


class Serializator:
    @staticmethod
    def get_level_json(level: Level):
        return {
            "name": level.name,
            "player_spawn": [level.player_spawn.x, level.player_spawn.y],
            "background_color": level.background_color,
            "objects": level.objects,
        }

    @staticmethod
    def get_entity_json(entity: Entity):
        type_ = None
        for key, value in ENTITY_FACTORY.items():
            if isinstance(entity, value):
                type_ = key
                break

        if type_ is None:
            raise ValueError(f"Unknown entity type: {type(entity)}")

        data = {
            "type": type_,
            "position": [entity.position.x, entity.position.y],
            "size": [entity.width, entity.height],
            "rotation": entity.rotation,
            "opacity": entity.opacity,
            "active": entity.active,
        }

        if hasattr(entity, "color_fill"):
            data["color_fill"] = list(entity.color_fill)

        if hasattr(entity, "color_border"):
            data["color_border"] = list(entity.color_border)
        if hasattr(entity, "color"):
            data["color"] = list(entity.color)
        if hasattr(entity, "activation_mode"):
            data["activation_mode"] = entity.activation_mode.name

        return data
