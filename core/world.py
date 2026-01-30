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

    def update(self, delta_time: float):
        for entity in self.entities:
            entity.update(delta_time)
            entity.update_hitbox()

            for other_entity in self.entities:
                if other_entity != entity:
                    if entity.hitbox.colliderect(other_entity.hitbox):
                        entity.on_entity_collision(other_entity)
