from .entity import Entity
from data import const
from .player import Player
from event import Event, EventType
import pygame

class Trigger(Entity):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.TRIGGER_SIZE[0],
                 height=const.TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.opacity = 0

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            self.activate(entity)

    def activate(self, player):
        pass


class ColorTrigger(Trigger):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.TRIGGER_SIZE[0],
                 height=const.TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.color = (0, 0, 0)

    def activate(self, player):
        self.world.level_background_color = self.color
