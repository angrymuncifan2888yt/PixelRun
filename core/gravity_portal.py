from pygame.math import Vector2
from .entity import Entity
from data import const
from .player import Player


class GravityPortal(Entity):
    def __init__(self, world, position: Vector2, width=const.GRAVITY_PORTAL_SIZE[0], height=const.GRAVITY_PORTAL_SIZE[1], rotation=0):
        super().__init__(
            world,
            position,
            const.GRAVITY_PORTAL_SIZE[0],
            const.GRAVITY_PORTAL_SIZE[1],
            rotation
        )
        self.hitbox.width = 40
        self.hitbox.height = 120

    def update_hitbox(self):
        self.hitbox.centerx = int(self.position.x + self.width / 2)
        self.hitbox.centery = int(self.position.y + self.height / 2)

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            self.handle_player(entity)

    def handle_player(self, player: Player):
        was_outside = not player.prev_rect.colliderect(self.hitbox)
        is_inside = player.hitbox.colliderect(self.hitbox)

        if was_outside and is_inside:
            self.apply(player)

    def apply(self, player: Player):
        player.reverse_gravity()