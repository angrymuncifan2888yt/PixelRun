from .trigger import Trigger, TriggerActivationMode
from data import const
import pygame

class ColorTrigger(Trigger):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.TRIGGER_SIZE[0],
                 height=const.TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.target_color = (0, 0, 0)
        self.activation_mode = TriggerActivationMode.ON_ENTER

    def activate(self, player):
        self.world.level_background_color = self.target_color

    def get_special_fields(self):
        return {
            "r": {"type": "int", "value": self.target_color[0]},
            "g": {"type": "int", "value": self.target_color[1]},
            "b": {"type": "int", "value": self.target_color[2]},
        }

    def apply_special_fields(self, data):
        try:
            self.target_color = (
                int(data.get("r", self.target_color[0])),
                int(data.get("g", self.target_color[1])),
                int(data.get("b", self.target_color[2])),
            )
        except:
            pass