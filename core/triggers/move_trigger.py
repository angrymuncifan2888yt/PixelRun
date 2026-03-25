from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationType


class MoveTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.target_offset = Vector2(0, 0)
        self.target_id = None
        self.transition_time = 0

        self._targets = []
        self._start_positions = {}
        self._elapsed = 0
        self._active = False

    def update(self, delta_time):
        super().update(delta_time)
        if not self._active:
            return

        self._elapsed += delta_time

        t = min(self._elapsed / self.transition_time, 1)

        for target in self._targets:
            start = self._start_positions[target]
            target.position = start + self.target_offset * t

        if t >= 1:
            self._active = False
    def activate(self, player):
        self._targets.clear()
        self._start_positions.clear()
        self._elapsed = 0

        if self.target_id is not None:
            self._targets = self.world.get_entities_by_id(self.target_id)

        if self.transition_time <= 0:
            for target in self._targets:
                target.position += self.target_offset
            return

        for target in self._targets:
            self._start_positions[target] = target.position.copy()

        self._active = True

    def get_special_fields(self):
        return {
            "offset_x": {"type": "float", "value": self.target_offset.x},
            "offset_y": {"type": "float", "value": self.target_offset.y},
            "target_id": {"type": "str", "value": self.target_id or ""},
            "transition_time": {"type": "float", "value": self.transition_time},
            "activation_type": {
                "type": "enum",
                "value": self.activation_type.name,
                "options": [e.name for e in TriggerActivationType]
            }
        }

    def apply_special_fields(self, data):
        try:
            self.target_offset.x = float(data.get("offset_x", self.target_offset.x))
            self.target_offset.y = float(data.get("offset_y", self.target_offset.y))
            self.target_id = data.get("target_id", None)
            self.transition_time = float(data.get("transition_time", self.transition_time))
            if "activation_type" in data:
                try:
                    self.activation_type = TriggerActivationType[data["activation_type"]]
                except:
                    pass
        except:
            pass