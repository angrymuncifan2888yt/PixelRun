import pygame
from .entity import Entity
from .player.player import Player


class Platform(Entity):
    def __init__(self, world, position: pygame.Vector2, width=100, height=100, rotation=0, color=(80, 180, 255)):
        super().__init__(world, position, width, height, rotation)
        self.color = color

    def update(self, delta_time: float):
        pass

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            entity.handle_platform_collision(self)

    def get_special_fields(self):
        return {
            "r": {"type": "int", "value": self.color[0]},
            "g": {"type": "int", "value": self.color[1]},
            "b": {"type": "int", "value": self.color[2]},
        }


    def apply_special_fields(self, data):
        try:
            self.color = (
                int(data.get("r", self.color[0])),
                int(data.get("g", self.color[1])),
                int(data.get("b", self.color[2])),
            )
        except:
            pass