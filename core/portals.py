from pygame.math import Vector2
from .entity import Entity
from .player import Player
from data import const

class Portal(Entity):
    def __init__(self, world, position: Vector2, width=const.PORTAL_SIZE[0], height=const.PORTAL_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            # проверяем вход игрока в портал с помощью prev_rect
            was_outside = not entity.prev_rect.colliderect(self.hitbox)
            is_inside = entity.hitbox.colliderect(self.hitbox)

            if was_outside and is_inside:
                self.apply(entity)

    def apply(self, player: Player):
        raise NotImplementedError


class GravityPortal(Portal):
    def apply(self, player: Player):
        player.reverse_gravity()


class UpsideDownPortal(Portal):
    def apply(self, player: Player):
        if not player.is_upside_down:
            player.reverse_gravity()


class NormalGravityPortal(Portal):
    def apply(self, player: Player):
        if player.is_upside_down:
            player.reverse_gravity()
