from ..entity import Entity
from data import const
from ..player.player import Player
from enum import Enum, auto
import pygame


class TriggerActivationType(Enum):
    ONCE_ON_ENTER = auto()
    ON_ENTER = auto()
    ON_STAY = auto()
    ALWAYS = auto()
    MANUAL = auto()


class Trigger(Entity):
    def __init__(self, world, position, width, height, rotation=0):
        super().__init__(world, position, width, height, rotation)

        self.opacity = 0
        self.activation_type = TriggerActivationType.ONCE_ON_ENTER
        self._activated = False

    def update(self, delta_time):
        if self.activation_type == TriggerActivationType.ALWAYS:
            self.activate(None)

    def on_entity_collision(self, entity):
        if not isinstance(entity, Player):
            return

        if self.activation_type == TriggerActivationType.MANUAL:
            return

        was_outside = not entity.prev_rect.colliderect(self.hitbox)
        is_inside = entity.hitbox.colliderect(self.hitbox)

        if self.activation_type == TriggerActivationType.ONCE_ON_ENTER:
            if not self._activated and was_outside and is_inside:
                self.activate(entity)
                self._activated = True

        elif self.activation_type == TriggerActivationType.ON_ENTER:
            if was_outside and is_inside:
                self.activate(entity)

        elif self.activation_type == TriggerActivationType.ON_STAY:
            if is_inside:
                self.activate(entity)

        if not is_inside:
            self._activated = False
    def activate(self, player):
        pass