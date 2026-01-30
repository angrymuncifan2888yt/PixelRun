from .entity import Entity
import pygame
from data import const
from .player import Player
from event import Event, EventType


class EndDoor(Entity):
    def __init__(self, world, position: pygame.Vector2, width=const.END_DOOR_SIZE[0], height=const.END_DOOR_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            event = Event(
                EventType.PLAYER_TOUCH_END_DOOR,
                {"position": self.position}
            )
            entity.world.event_bus.emit(event)
