import pygame
from core import Entity
from util import Camera

import pygame
from core import Entity
from util import Camera

_transform_cache: dict[tuple[int, bool, int, int], pygame.Surface] = {}


def get_transformed(
    surface: pygame.Surface,
    *,
    flip_x: bool = False,
    angle: int = 0,
    opacity: int = 255
) -> pygame.Surface:
    key = (id(surface), flip_x, angle, opacity)
    cached = _transform_cache.get(key)
    if cached:
        return cached

    result = surface

    if flip_x:
        result = pygame.transform.flip(result, True, False)

    if angle != 0:
        result = pygame.transform.rotate(result, angle)

    if opacity < 255:
        result = result.copy()
        result.set_alpha(opacity)

    _transform_cache[key] = result
    return result


def get_entity_screen_pos(entity: Entity, camera: Camera | None):
    return camera.get_screen_position(entity.position) if camera else entity.position


def blit_centered(screen, surface, pos, width, height):
    rect = surface.get_rect(
        center=(int(pos.x + width / 2), int(pos.y + height / 2))
    )
    screen.blit(surface, rect)
