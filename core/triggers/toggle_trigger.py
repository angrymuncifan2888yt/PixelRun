from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class ToggleTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ONCE
        self.toggle = None
        self.target_id = None

    def activate(self, player):
        if self.target_id is None:
            return

        for entity in self.world.get_entities_by_id(self.target_id):
            to_set = not entity.active
            if self.toggle is True:
                to_set = True
            elif self.toggle is False:
                to_set = False
            entity.active = to_set

    def get_special_fields(self):
        return {
            "toggle": {"type": "bool", "value": self.toggle if self.toggle is not None else -1},
            "target_id": {"type": "str", "value": self.target_id or ""}
        }

    def apply_special_fields(self, data):
        try:
            toggle = data.get("toggle", -1)
            if toggle == -1:
                self.toggle = None
            else:
                self.toggle = bool(toggle)

            self.target_id = data.get("target_id", None)
        except:
            pass