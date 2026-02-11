from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode


class ToggleTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ONCE
        self.toggle = None
        self.target_ids = []

    def activate(self, player):
        for group_id in self.target_ids:
            for entity in self.world.get_entities_by_id(group_id):
                to_set = not entity.active
                if self.toggle == True:
                    to_set = True
                elif self.toggle == False:
                    to_set = False
                entity.active = to_set