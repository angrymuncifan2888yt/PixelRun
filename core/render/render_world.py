from .render_entity import render_entity
from .render_hitbox import render_hitbox
from ..world import World
from util import Camera
import pygame


def render_world(screen: pygame.Surface, world: World, camera: Camera=None, render_hitbox_: bool = False):
    for entity in world.entities:
        render_entity(screen, entity, camera)

        if render_hitbox_:
            render_hitbox(screen, entity.hitbox, camera)
