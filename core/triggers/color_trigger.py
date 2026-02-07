from .trigger import Trigger, TriggerActivationMode
from data import const
import pygame

class ColorTrigger(Trigger):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.TRIGGER_SIZE[0],
                 height=const.TRIGGER_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.color = (0, 0, 0)
        self.activation_mode = TriggerActivationMode.ON_ENTER

    def activate(self, player):
        self.world.level_background_color = self.color
