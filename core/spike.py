import pygame
from .entity import Entity
from .player import Player
from data import const


class Spike(Entity):
    def __init__(self, world, position: pygame.Vector2,
                 width=const.SPIKE_SIZE[0],
                 height=const.SPIKE_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)

        self.hitbox.width = int(self.width * 0.25)
        self.hitbox.height = int(self.height * 0.6)
        self.color_fill = (0, 0, 0)
        self.color_border = (255, 255, 255)

    def update_hitbox(self):
        self.hitbox.width = int(self.width * 0.25)
        self.hitbox.height = int(self.height * 0.6)

        self.hitbox.center = (
            int(self.position.x + self.width / 2),
            int(self.position.y + self.height / 2),
        )

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            entity.kill()
