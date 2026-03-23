from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class OpacityTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.target_opacity = 0
        self.target_id = None
        self.transition_time = 0

        self._targets = []
        self._start_opacities = {}
        self._elapsed = 0
        self._active = False

    def activate(self, player):
        self._targets.clear()
        self._start_opacities.clear()
        self._elapsed = 0

        if self.target_id is not None:
            self._targets = self.world.get_entities_by_id(self.target_id)

        if self.transition_time <= 0:
            for target in self._targets:
                target.opacity = self.target_opacity
            return

        for target in self._targets:
            self._start_opacities[target] = target.opacity

        self._active = True

    def update(self, delta_time):
        if not self._active:
            return

        self._elapsed += delta_time

        t = min(self._elapsed / self.transition_time, 1)

        for target in self._targets:
            start = self._start_opacities[target]
            target.opacity = int(start + (self.target_opacity - start) * t)

        if t >= 1:
            self._active = False
    def get_special_fields(self):
        return {
            "target_opacity": {"type": "int", "value": self.target_opacity},
            "target_id": {"type": "str", "value": self.target_id or ""},
            "transition_time": {"type": "float", "value": self.transition_time},
        }

    def apply_special_fields(self, data):
        try:
            self.target_opacity = int(data.get("target_opacity", self.target_opacity))
            self.target_id = data.get("target_id", None)
            self.transition_time = float(data.get("transition_time", self.transition_time))
        except:
            pass