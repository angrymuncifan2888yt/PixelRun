import pygame
from core import Entity
from util import Camera

_transform_cache: dict[tuple[int, int, int, bool, int, int], pygame.Surface] = {}


def get_transformed(
    surface: pygame.Surface,
    *,
    width: int,
    height: int,
    flip_x: bool = False,
    angle: int = 0,
    opacity: int = 255,
) -> pygame.Surface:
    key = (id(surface), width, height, flip_x, angle, opacity)
    cached = _transform_cache.get(key)
    if cached:
        return cached

    result = surface

    # 🔹 SCALE
    if surface.get_width() != width or surface.get_height() != height:
        result = pygame.transform.smoothscale(result, (width, height))

    # 🔹 FLIP
    if flip_x:
        result = pygame.transform.flip(result, True, False)

    # 🔹 ROTATE
    if angle != 0:
        result = pygame.transform.rotate(result, angle)

    # 🔹 OPACITY
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
