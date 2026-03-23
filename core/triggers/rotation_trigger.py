from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class RotationTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.rotation_a = 0
        self.rotation_b = 90
        self.target_id = None
        self.transition_time = 0

        self._targets = []
        self._start_rotations = {}
        self._elapsed = 0
        self._active = False
        self._state = False

    def update(self, delta_time):
        if not self._active:
            return

        self._elapsed += delta_time

        t = min(self._elapsed / self.transition_time, 1)

        for target in self._targets:
            start = self._start_rotations[target]
            target.rotation = start + (self._target_rotation - start) * t

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

        self._state = not self._state
        target_rotation = self.rotation_b if self._state else self.rotation_a

        if self.transition_time <= 0:
            for target in self._targets:
                target.rotation = target_rotation
            return

        for target in self._targets:
            self._start_rotations[target] = target.rotation

        self._target_rotation = target_rotation
        self._active = True

    def get_special_fields(self):
        return {
            "rotation_a": {"type": "float", "value": self.rotation_a},
            "rotation_b": {"type": "float", "value": self.rotation_b},
            "target_id": {"type": "str", "value": self.target_id or ""},
            "transition_time": {"type": "float", "value": self.transition_time},
        }

    def apply_special_fields(self, data):
        try:
            self.rotation_a = float(data.get("rotation_a", self.rotation_a))
            self.rotation_b = float(data.get("rotation_b", self.rotation_b))
            self.target_id = data.get("target_id", None)
            self.transition_time = float(data.get("transition_time", self.transition_time))
        except:
            pass