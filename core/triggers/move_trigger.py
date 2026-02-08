from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class MoveTrigger(Trigger):
    def __init__(self, world, position: Vector2, width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ONCE
        self.target_offset = Vector2(0, 0)
        self.target_ids = []
        self.transition_time = 0

        self._targets = []
        self._start_positions = {}
        self._elapsed = 0
        self._active = False

    def activate(self, player):
        self._targets.clear()
        self._start_positions.clear()
        self._elapsed = 0

        if self.target_ids:
            for id_ in self.target_ids:
                self._targets.extend(self.world.get_entities_by_id(id_))

        if self.transition_time <= 0:
            for target in self._targets:
                target.position += self.target_offset
            self._active = False
            return

        for target in self._targets:
            self._start_positions[target] = target.position.copy()

        self._active = True

    def update(self, delta_time):
        if not self._active:
            return

        self._elapsed += delta_time
        t = min(self._elapsed / self.transition_time, 1)

        for target in self._targets:
            start = self._start_positions[target]
            target.position = start + self.target_offset * t

        if t >= 1:
            self._active = False
