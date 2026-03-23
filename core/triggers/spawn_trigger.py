from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode
from util import Timer

class SpawnTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1],
                 rotation=0, delay_duration=0.5):
        super().__init__(world, position, width, height, rotation)
        self.target_id = None
        self.delay = Timer(delay_duration)
        self._waiting = False
        self._player = None
        self._activated = False

    def activate(self, player):
        if self._activated or self._waiting:
            return

        self._player = player
        self.delay.reset()
        self._waiting = True

    def update(self, delta_time):
        if not self._waiting:
            return

        self.delay.update(delta_time)
        if self.delay.finished:
            self._spawn(self._player)
            self._waiting = False
            self._player = None
            self._activated = True

    def _spawn(self, player):
        if self.target_id is None:
            return

        for trigger in self.world.get_entities_by_id(self.target_id):
            if isinstance(trigger, Trigger):
                trigger.activate(player)

    def get_special_fields(self):
        return {
            "target_id": {"type": "str", "value": self.target_id or ""},
            "delay": {"type": "float", "value": self.delay.duration}
        }

    def apply_special_fields(self, data):
        try:
            self.target_id = data.get("target_id", None)
            self.delay.duration = float(data.get("delay", self.delay.duration))
        except:
            pass