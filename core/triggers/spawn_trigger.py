from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationType


class SpawnTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1],
                 rotation=0, delay=0.0):
        super().__init__(world, position, width, height, rotation)

        self.target_id = None
        self.delay = max(0.0, delay)

        self._waiting = False
        self._elapsed = 0.0
        self._player = None

    def activate(self, player):
        if self._waiting:
            return

        # 🔥 если delay = 0 → сразу активируем
        if self.delay == 0:
            self._spawn(player)
            return

        self._player = player
        self._elapsed = 0.0
        self._waiting = True

    def update(self, delta_time):
        super().update(delta_time)

        if not self._waiting:
            return

        self._elapsed += delta_time

        if self._elapsed >= self.delay:
            self._spawn(self._player)
            self._waiting = False
            self._player = None

    def _spawn(self, player):
        if self.target_id is None:
            return

        for trigger in self.world.get_entities_by_id(self.target_id):
            if isinstance(trigger, Trigger):
                trigger.activate(player)

    def get_special_fields(self):
        return {
            "target_id": {"type": "str", "value": self.target_id or ""},
            "delay": {"type": "float", "value": self.delay},
            "activation_type": {
                "type": "enum",
                "value": self.activation_type.name,
                "options": [e.name for e in TriggerActivationType]
            }
        }

    def apply_special_fields(self, data):
        try:
            self.target_id = data.get("target_id", None)
            self.delay = float(data.get("delay", self.delay))

            if "activation_type" in data:
                try:
                    self.activation_type = TriggerActivationType[data["activation_type"]]
                except:
                    pass
        except:
            pass