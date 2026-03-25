from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationType
from enum import Enum, auto

class ToggleMode(Enum):
    ON = auto()
    OFF = auto()
    TOGGLE = auto()

class ToggleTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.toggle = ToggleMode.TOGGLE
        self.target_id = None

    def activate(self, player):
        if self.target_id is None:
            return

        for entity in self.world.get_entities_by_id(self.target_id):
            if self.toggle == ToggleMode.ON:
                entity.active = True

            elif self.toggle == ToggleMode.OFF:
                entity.active = False

            elif self.toggle == ToggleMode.TOGGLE:
                entity.active = not entity.active
    def get_special_fields(self):
        return {
            "toggle": {
                "type": "enum",
                "value": self.toggle.name,
                "options": [e.name for e in ToggleMode]
            },
            "target_id": {"type": "str", "value": self.target_id or ""},
            "activation_type": {
                "type": "enum",
                "value": self.activation_type.name,
                "options": [e.name for e in TriggerActivationType]
            }
        }

    def apply_special_fields(self, data):
        try:
            if "toggle" in data:
                try:
                    self.toggle = ToggleMode[data["toggle"]]
                except:
                    pass
            self.target_id = data.get("target_id", None)
            if "activation_type" in data:
                try:
                    self.activation_type = TriggerActivationType[data["activation_type"]]
                except:
                    pass
        except:
            pass