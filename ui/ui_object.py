import pygame

class UiObject:
    def __init__(self, position):
        # Всегда Vector2
        if isinstance(position, tuple):
            self.position = pygame.Vector2(position)
        else:
            self.position = position
        self.parent = None

    def get_global_position(self):
        # Возвращаем копию Vector2, суммируя с родителем
        pos = self.position.copy()
        if self.parent:
            pos += self.parent.get_global_position()
        return pos

    def handle_pygame_event(self, pygame_event):
        pass

    def update(self, delta, **kwargs):
        pass

    def draw(self, screen):
        pass

    def center_by_x(self, width: int):
        pass

    def center_by_y(self, height: int):
        pass