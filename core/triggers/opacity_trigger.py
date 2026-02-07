from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class OpacityTrigger(Trigger):
    def __init__(self, world, position: Vector2, width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ON_ENTER
        self.target_opacity = 0
        self.target_ids = []

    def activate(self, player):
        targets = []
        if self.target_ids:
            for id_ in self.target_ids:
                entities = self.world.get_entities_by_id(id_)
                targets.extend(entities)

        for target in targets:
            target.opacity = self.target_opacity
