from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class MoveTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ONCE

        self.target_offset = Vector2(0, 0)
        self.target_id = None
        self.transition_time = 0

        self._targets = []
        self._start_positions = {}
        self._elapsed = 0
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