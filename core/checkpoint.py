import pygame
from .entity import Entity
from .player import Player
from data import const


class Checkpoint(Entity):
    def __init__(self, world, position: pygame.Vector2, rotation=0):
        super().__init__(world, position, *const.CHECKPOINT_SIZE, rotation)
