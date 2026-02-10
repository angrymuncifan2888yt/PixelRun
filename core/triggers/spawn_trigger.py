from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode
from util import Timer


class SpawnTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ON_ENTER

        self.target_ids = []
        self.delay = Timer(0.5)
        self._can_spawn = True

    def activate(self, player):
        if not self._can_spawn:
            return

        self._spawn(player)
        self._can_spawn = False
        self.delay.reset()

    def update(self, delta_time):
        if self._can_spawn:
            return

        self.delay.update(delta_time)
        if self.delay.finished:
            self._can_spawn = True

    def _spawn(self, player):
        for group_id in self.target_ids:
            for trigger in self.world.get_entities_by_id(group_id):
                if isinstance(trigger, Trigger):
                    trigger.activate(player)
                    trigger._activated = True
