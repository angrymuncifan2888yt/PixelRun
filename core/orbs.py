from pygame import Vector2
from .entity import Entity
from data.const import ORB_SIZE
from .player.player import Player
from event import EventType, Event


class Orb(Entity):
    def __init__(self, world, position: Vector2, width=ORB_SIZE[0], height=ORB_SIZE[1], rotation=0):
        super().__init__(world, position, width, height, rotation)

    def on_entity_collision(self, entity):
        if isinstance(entity, Player):
            if entity.is_clicking:
                self.activate(entity)
                self.world.event_bus.emit(Event(EventType.PLAYER_JUMP, {}))

    # To be made in child classes
    def activate(self, player: Player):
        pass


class JumpOrb(Orb):
    def activate(self, player: Player):
        player.on_ground = True
        player.jump()


class GravityOrb(Orb):
    def activate(self, player: Player):
        player.reverse_gravity()