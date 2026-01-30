from pygame import Vector2
from core import *
from .entity_factory import ENTITY_FACTORY
from .deserializator import Deserializator

class Level:
    def __init__(self, name="", player_spawn=Vector2(0, 0), background_color=(100, 100, 100), objects=None):
        self.name = name
        self.player_spawn = player_spawn
        self.background_color = background_color
        self.objects = objects or []

    def load_to_world(self, world, player):
        world.entities.clear()

        player.position = self.player_spawn.copy()
        player.base_spawn_position = self.player_spawn.copy()
        player.world = world

        for obj in self.objects:
            entity = Deserializator.load_entity(obj, world)
            world.add_entity(entity)

        world.add_entity(player)
