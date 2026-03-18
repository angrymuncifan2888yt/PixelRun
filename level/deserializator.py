from pygame import Vector2
from .entity_factory import ENTITY_FACTORY
from core import Trigger, TriggerActivationMode
from util import Timer


class Deserializator:
    @staticmethod
    def load_level(data: dict) -> "Level":
        from .level import Level
        name = data.get("name", "Unnamed Level")
        player_spawn = data.get("player_spawn", Vector2(0, 0))
        if player_spawn:
            player_spawn = Vector2(player_spawn)
            
        background_color = data.get("background_color", [0, 0, 0])
        objects = data.get("objects", [])
        return Level(
            name, player_spawn, background_color, objects
        )

    @staticmethod
    def load_entity(entity_json: dict, world):
        entity_class = ENTITY_FACTORY[entity_json["type"]]

        kvargs = {
            "world": world,
            "position": Vector2(entity_json["position"]),
        }

        if entity_json.get("size"):
            kvargs["width"] = entity_json["size"][0]
            kvargs["height"] = entity_json["size"][1]

        if entity_json.get("rotation") is not None:
            kvargs["rotation"] = entity_json["rotation"]

        entity = entity_class(**kvargs)

        if entity_json.get("target_offset"):
            entity.target_offset = Vector2(entity_json["target_offset"])
            
        if entity_json.get("delay"):
            if isinstance(entity_json.get("delay"), int) or isinstance(entity_json.get("delay"), float):
                entity.delay = Timer(entity_json["delay"])
        
        if entity_json.get("color_fill"):
            entity.color_fill = tuple(entity_json["color_fill"])

        if entity_json.get("color"):
            entity.color = tuple(entity_json["color"])

        if entity_json.get("target_color"):
            entity.target_color = tuple(entity_json["target_color"])

        if entity_json.get("color_border"):
            entity.color_border = tuple(entity_json["color_border"])

        if entity_json.get("id"):
            entity.id = list(entity_json["id"])

        # Новый формат
        if entity_json.get("target_id") is not None:
            entity.target_id = entity_json["target_id"]

        # Старый формат (fallback)
        elif entity_json.get("target_ids"):
            ids = entity_json["target_ids"]
            if isinstance(ids, list) and len(ids) > 0:
                entity.target_id = ids[0]
        if entity_json.get("toggle"):
            entity.toggle = entity_json["toggle"]
    
        if entity_json.get("target_rotation"):
            entity.target_rotation = float(entity_json["target_rotation"])
            
        if entity_json.get("opacity"):
            entity.opacity = int(entity_json["opacity"])

        else:
            if isinstance(entity, Trigger):
                entity.opacity = 0
            else:
                entity.opacity = 255

        if entity_json.get("target_opacity") is not None:
            entity.target_opacity = int(entity_json["target_opacity"])
        if entity_json.get("transition_time") is not None:
            entity.transition_time = float(entity_json["transition_time"])
        if entity_json.get("active") is not None:
            entity.active = entity_json["active"]

        mode = entity_json.get("activation_mode")
        if mode:
            entity.activation_mode = TriggerActivationMode[mode]

        return entity
