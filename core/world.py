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

        self.cell_size = 200
        self.grid = {}
        self.large_entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

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
        result = []
        for entity in self.entities:
            if id in entity.id:
                result.append(entity)
        return result

    def get_nearest_entities(self, position: pygame.Vector2, radius: float) -> List[Entity]:
        result = []
        radius_sq = radius * radius

        for entity in self.entities:
            if not entity.active:
                continue

            rect = entity.hitbox

            closest_x = max(rect.left, min(position.x, rect.right))
            closest_y = max(rect.top, min(position.y, rect.bottom))

            dx = position.x - closest_x
            dy = position.y - closest_y

            if dx * dx + dy * dy <= radius_sq:
                result.append(entity)

        return result

    def _get_cells_for_rect(self, rect: pygame.Rect):
        min_x = rect.left // self.cell_size
        max_x = rect.right // self.cell_size
        min_y = rect.top // self.cell_size
        max_y = rect.bottom // self.cell_size

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                yield (x, y)

    def _is_large(self, rect: pygame.Rect):
        return (
            rect.width > self.cell_size * 2 or
            rect.height > self.cell_size * 2
        )

    def _build_grid(self):
        self.grid.clear()
        self.large_entities.clear()

        for entity in self.entities:
            if not entity.active:
                continue

            rect = entity.hitbox

            if self._is_large(rect):
                self.large_entities.append(entity)
                continue

            for cell in self._get_cells_for_rect(rect):
                if cell not in self.grid:
                    self.grid[cell] = []

                self.grid[cell].append(entity)

    def update_entities(self, entities: List[Entity], delta_time: float):
        updated = 0

        self._build_grid()

        entities_copy = entities[:]

        checked_pairs = set()

        for entity in entities_copy:
            if not entity.active:
                continue

            entity.update(delta_time)
            updated += 1

            rect = entity.hitbox

            # 🔹 Проверка через grid
            for cell in self._get_cells_for_rect(rect):
                for other in self.grid.get(cell, []):
                    if other is entity or not other.active:
                        continue

                    pair = (id(entity), id(other))
                    if pair in checked_pairs:
                        continue

                    checked_pairs.add(pair)

                    if rect.colliderect(other.hitbox):
                        entity.on_entity_collision(other)

            # 🔸 Проверка с большими объектами
            for other in self.large_entities:
                if other is entity or not other.active:
                    continue

                pair = (id(entity), id(other))
                if pair in checked_pairs:
                    continue

                checked_pairs.add(pair)

                if rect.colliderect(other.hitbox):
                    entity.on_entity_collision(other)

        return updated