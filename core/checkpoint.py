import pygame
from .entity import Entity
from .player import Player
from data import const


class Checkpoint(Entity):
    def __init__(self, world, position: pygame.Vector2, rotation=0):
        super().__init__(world, position, *const.CHECKPOINT_SIZE, rotation)
        self.activated = False

    def on_entity_collision(self, entity):
        if self.activated:
            return

        if isinstance(entity, Player):
            was_outside = not entity.prev_rect.colliderect(self.hitbox)
            is_inside = entity.hitbox.colliderect(self.hitbox)

            if was_outside and is_inside:
                self.activate(entity)

    def activate(self, player: Player):
        self.activated = True
        self.active = False
        player.current_checkpoint = self
        self.opacity /= 2
