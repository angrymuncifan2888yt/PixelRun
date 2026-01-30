import pygame

class Camera:
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height
        self.smooth = 0.1

    def update(self, target_pos: pygame.Vector2):
        target_x = target_pos.x - self.width / 2
        target_y = target_pos.y - self.height / 2

        self.position.x += (target_x - self.position.x) * self.smooth
        self.position.y += (target_y - self.position.y) * self.smooth

    def get_screen_position(self, world_pos: pygame.Vector2):
        return world_pos - self.position
