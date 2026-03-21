from pygame.math import Vector2
from .entity import Entity
from data import const
from .player import Player


class JumpPad(Entity):
    def __init__(self, world, position: Vector2, width=const.JUMP_PAD_SIZE[0],
                 height=const.JUMP_PAD_SIZE[1], rotation=0, color=(255, 255, 0)):
        super().__init__(
            world,
            position,
            width, height,
            rotation
        )
        self.color = color
        self.power = 1350

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            entity.on_ground = True
            prev = entity.jump_force
            entity.jump_force = self.power # Jump pad power
            entity.jump()
            entity.jump_force = prev

    def get_special_fields(self):
        return {
            "r": {"type": "int", "value": self.color[0]},
            "g": {"type": "int", "value": self.color[1]},
            "b": {"type": "int", "value": self.color[2]},
            "power": {"type": "int", "value": self.power}
        }


    def apply_special_fields(self, data):
        try:
            self.color = (
                int(data.get("r", self.color[0])),
                int(data.get("g", self.color[1])),
                int(data.get("b", self.color[2])),
            )
            self.power = int(data.get("power", self.power))
        except:
            pass