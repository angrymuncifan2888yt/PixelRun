import pygame
import math

class Camera:
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height

        self.smooth = 8.0  # fallback значение

    def update(self, target_pos: pygame.Vector2, delta_time: float):
        # 🔥 ЛЕНИВЫЙ ИМПОРТ (разрывает цикл)
        from data import PlayerData
        self.smooth = PlayerData.CAMERA_SPEED

        target_x = target_pos.x - self.width / 2
        target_y = target_pos.y - self.height / 2

        factor = 1 - math.exp(-self.smooth * delta_time)

        self.position.x += (target_x - self.position.x) * factor
        self.position.y += (target_y - self.position.y) * factor

    def get_screen_position(self, world_pos: pygame.Vector2):
        return world_pos - self.position

    def is_object_visible(self, pos: pygame.Vector2, w: float, h: float) -> bool:
        cam_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        obj_rect = pygame.Rect(pos.x, pos.y, w, h)
        return cam_rect.colliderect(obj_rect)