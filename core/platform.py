import pygame
from .entity import Entity
from .player import Player


class Platform(Entity):
    def __init__(self, world, position: pygame.Vector2, width=200, height=200, rotation=0, color=(80, 180, 255)):
        super().__init__(world, position, width, height, rotation)
        self.color = color

    def update(self, delta_time: float):
        pass

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            entity.handle_platform_collision(self)
