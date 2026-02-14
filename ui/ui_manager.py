import pygame
from .ui_object import UiObject


class UiManager:
    def __init__(self):
        self.ui_objects = []

    def add_ui_object(self, obj: UiObject):
        self.ui_objects.append(obj)

    def remove_ui_object(self, obj: UiObject):
        if obj in self.ui_objects:
            self.ui_objects.remove(obj)

    def is_mouse_over_ui(self, mouse_pos: pygame.Vector2):
        for obj in self.ui_objects:
            if hasattr(obj, "get_rect"):
                rect = obj.get_rect()
                if rect and rect.collidepoint(mouse_pos):
                    return True
        return False

    def handle_pygame_event(self, event: pygame.event.Event):
        for obj in self.ui_objects:
            obj.handle_pygame_event(event)

    def update(self, delta_time: float, **kwargs):
        for obj in self.ui_objects:
            obj.update(delta_time, **kwargs)

    def draw(self, screen):
        for obj in self.ui_objects:
            obj.draw(screen)
