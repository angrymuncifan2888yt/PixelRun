from ..entity import Entity
from data import const
from ..player import Player
from enum import Enum, auto
import pygame


class TriggerActivationMode(Enum):
    ONCE_ON_ENTER = auto()
    ON_ENTER = auto()
    ON_STAY = auto()
    ALWAYS = auto()
    MANUAL = auto()


class Trigger(Entity):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.TRIGGER_SIZE[0],
                 height=const.TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)

        self.opacity = 0
        self.activation_type = TriggerActivationMode.ONCE_ON_ENTER
        self._activated = False

    def update(self, delta_time):
        if self.activation_type == TriggerActivationMode.ALWAYS:
            if not self._activated:
                self.activate(None)
                self._activated = True

    def on_entity_collision(self, entity):
        if not isinstance(entity, Player):
            return

        if self.activation_type == TriggerActivationMode.MANUAL:
            return

        was_outside = not entity.prev_rect.colliderect(self.hitbox)
        is_inside = entity.hitbox.colliderect(self.hitbox)

        # 🔹 ONCE_ON_ENTER
        if self.activation_type == TriggerActivationMode.ONCE_ON_ENTER:
            if not self._activated and was_outside and is_inside:
                self.activate(entity)
                self._activated = True

        # 🔹 ON_ENTER
        elif self.activation_type == TriggerActivationMode.ON_ENTER:
            if was_outside and is_inside:
                self.activate(entity)

        # 🔹 ON_STAY
        elif self.activation_type == TriggerActivationMode.ON_STAY:
            if is_inside:
                self.activate(entity)

    def activate(self, player):
        pass