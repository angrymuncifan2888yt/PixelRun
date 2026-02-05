from typing import List
from .entity import Entity
from math import inf
from .checkpoint import Checkpoint
import pygame
from event import EventBus


class World:
    def __init__(self):
        self.entities: List[Entity] = []
        self.event_bus = EventBus()
        self.level_background_color = [0, 0, 0]
    
    def get_nearest_checkpoint(self, position: pygame.Vector2) -> Checkpoint | None:
        nearest = None
        min_dist = inf

        for entity in self.entities:
            if isinstance(entity, Checkpoint):
                dist = position.distance_to(entity.position)
                if dist < min_dist:
                    min_dist = dist
                    nearest = entity

        return nearest

    def add_entity(self, entity):
        self.entities.append(entity)
    
    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def update_hitboxes(self):
        for entity in self.entities:
            entity.update_hitbox()

    def update(self, delta_time: float):
        self.update_hitboxes()

        for entity in self.entities:
            if entity.active:
                entity.update(delta_time)

                for other_entity in self.entities:
                    if other_entity != entity:
                        if entity.hitbox.colliderect(other_entity.hitbox):
                            if other_entity.active:
                                entity.on_entity_collision(other_entity)
