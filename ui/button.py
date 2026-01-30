import pygame
from .ui_object import UiObject


class Button(UiObject):
    def __init__(self, position, hitbox_size, callback=None):
        super().__init__(position)
        self.callback = callback
        self.hitbox = pygame.Rect(position, hitbox_size)

    def is_mouse_on_button(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.hitbox.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_mouse_on_button()
        return False

    def handle_pygame_event(self, pygame_event):
        if self.is_clicked(pygame_event):
            if callable(self.callback):
                self.callback()
