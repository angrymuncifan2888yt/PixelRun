import pygame
from util import Camera


def render_hitbox(screen, hitbox: pygame.Rect, camera: Camera = None):
    rect = hitbox.copy()

    if camera:
        rect.topleft -= camera.position

    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
