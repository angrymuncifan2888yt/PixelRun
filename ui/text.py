import pygame
from .ui_object import UiObject


class Text(UiObject):
    def __init__(self, position, font: pygame.font.Font, text, color=(255, 255, 255)):
        super().__init__(position)
        self.color = color
        self.font = font
        self.text = text

    def draw(self, screen):
        render = self.font.render(self.text, True, self.color)
        screen.blit(render, self.get_global_position())

    def center_by_x(self, width: int):
        render = self.font.render(self.text, True, self.color)
        self.position.x = (width - render.get_width()) // 2

    def center_by_y(self, height: int):
        render = self.font.render(self.text, True, self.color)
        self.position.y = (height - render.get_height()) // 2
