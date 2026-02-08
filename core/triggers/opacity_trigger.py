from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class OpacityTrigger(Trigger):
    def __init__(self, world, position: Vector2, width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ON_ENTER
        self.target_opacity = 0
        self.target_ids = []
        self.transition_time = 0

        self._targets = []
        self._start_opacities = {}
        self._elapsed = 0
        self._active = False

    def activate(self, player):
        self._targets.clear()
        self._start_opacities.clear()
        self._elapsed = 0

        if self.target_ids:
            for id_ in self.target_ids:
                self._targets.extend(self.world.get_entities_by_id(id_))

        if self.transition_time <= 0:
            for target in self._targets:
                target.opacity = self.target_opacity
            self._active = False
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
            target.opacity = start + (self.target_opacity - start) * t

        if t >= 1:
            self._active = False
