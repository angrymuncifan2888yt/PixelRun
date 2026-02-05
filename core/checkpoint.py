import pygame
from .entity import Entity
from .player import Player
from data import const


class Checkpoint(Entity):
    def __init__(self, world, position: pygame.Vector2, width=const.CHECKPOINT_SIZE[0]
                 ,height=const.CHECKPOINT_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)
        self.activated = False
        self.gravity_dir = 1
        self.level_background_color = []

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

        # Save params
        self.gravity_dir = player.gravity_dir
        self.level_background_color = self.world.level_background_color
