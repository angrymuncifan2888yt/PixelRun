from ..entity import Entity
from data import const
from ..player import Player
from event import Event, EventType
from enum import Enum, auto
import pygame


class TriggerActivationMode(Enum):
    ALWAYS = auto()       # активируется каждый тик в коллизии
    ONCE = auto()         # активируется один раз
    ON_ENTER = auto()     # активируется при входе (вышел → зашёл)

class Trigger(Entity):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.TRIGGER_SIZE[0],
                 height=const.TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.opacity = 0
        self.activation_mode = TriggerActivationMode.ONCE
        self._activated = False

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            if self.activation_mode == TriggerActivationMode.ONCE:
                if not self._activated:
                    self.activate(entity)
                    self._activated = True
            elif self.activation_mode == TriggerActivationMode.ALWAYS:
                self.activate(entity)

            elif self.activation_mode == TriggerActivationMode.ON_ENTER:
                was_outside = not entity.prev_rect.colliderect(self.hitbox)
                is_inside = entity.hitbox.colliderect(self.hitbox)

                if was_outside and is_inside:
                    self.activate(entity)


    def activate(self, player):
        pass
