from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationType


class RotationTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)

        self.target_rotation = 90
        self.target_id = None
        self.transition_time = 0

        self._targets = []
        self._start_rotations = {}
        self._elapsed = 0
        self._active = False

    def update(self, delta_time):
        if not self._active:
            return

        self._elapsed += delta_time

        t = min(self._elapsed / self.transition_time, 1)

        for target in self._targets:
            start = self._start_rotations[target]
            target.rotation = start + self.target_rotation * t

        if t >= 1:
            self._active = False

    def activate(self, player):
        if self._active:
            return

        self._targets.clear()
        self._start_rotations.clear()
        self._elapsed = 0

        if self.target_id is not None:
            self._targets = self.world.get_entities_by_id(self.target_id)

        if not self._targets:
            return

        # 🔥 МГНОВЕННОЕ ВРАЩЕНИЕ
        if self.transition_time <= 0:
            for target in self._targets:
                target.rotation += self.target_rotation
            return

        # 🔥 ПЛАВНОЕ ВРАЩЕНИЕ
        for target in self._targets:
            self._start_rotations[target] = target.rotation

        self._active = True

    def get_special_fields(self):
        return {
            "target_rotation": {"type": "float", "value": self.target_rotation},
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
            if "target_rotation" in data:
                self.target_rotation = float(data["target_rotation"])

            if "target_id" in data:
                self.target_id = data["target_id"] or None

            if "transition_time" in data:
                self.transition_time = float(data["transition_time"])

            if "activation_type" in data:
                try:
                    self.activation_type = TriggerActivationType[data["activation_type"]]
                except:
                    pass
        except:
            pass