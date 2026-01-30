from pygame import Vector2
from .entity_factory import ENTITY_FACTORY


class Deserializator:
    @staticmethod
    def load_level(data: dict) -> "Level":
        from .level import Level
        from pygame import Vector2
        return Level(
            name=data["name"],
            player_spawn=Vector2(*data["player_spawn"]),
            background_color=data["background_color"],
            objects=data["objects"]
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
        if entity_json.get("rotation"):
            kvargs["rotation"] = entity_json["rotation"]
        if entity_json.get("color"):
            kvargs["color"] = entity_json["color"]

        return entity_class(**kvargs)
    