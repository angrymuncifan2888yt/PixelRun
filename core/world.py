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

    def get_entities_by_id(self, id: str):
        list_ = []
        for entity in self.entities:
            if id in entity.id:
                list_.append(entity)
        return list_

    def add_entity(self, entity):
        self.entities.append(entity)
    
    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            
    def get_nearest_entities(
        self,
        position: pygame.Vector2,
        radius: float
    ) -> List[Entity]:
        result = []
        radius_sq = radius * radius

        for entity in self.entities:
            try:
                rect = entity.hitbox

                closest_x = max(rect.left, min(position.x, rect.right))
                closest_y = max(rect.top, min(position.y, rect.bottom))

                dx = position.x - closest_x
                dy = position.y - closest_y

                dist_sq = dx * dx + dy * dy

                if dist_sq <= radius_sq:
                    result.append(entity)

            except Exception as e:
                pass

        return result

    def update_all_hitboxes(self):
        updated = 0
        for entity in self.entities:
            entity.update_hitbox()
            updated += 1
        return updated

    def update_entities(self, entities: List[Entity], delta_time: float):
        # Actual update
        updated = 0
        for entity in entities:
            try:
                if entity.active:
                    entity.update(delta_time)
                    updated += 1
                    for other in entities:
                        if other is entity or not other.active:
                            continue

                        if entity.hitbox.colliderect(other.hitbox):
                            entity.on_entity_collision(other)

            except Exception as e:
                pass
            
        return updated
