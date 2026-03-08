import pygame
from .ui_object import UiObject


class LineEdit(UiObject):

    def __init__(self, position, size, font, max_length=32):
        super().__init__(position)

        self.size = size
        self.font = font
        self.max_length = max_length

        self.text = ""
        self.active = False

        self.hitbox = pygame.Rect(position, size)

        self.bg_color = (40, 40, 40)
        self.border_color = (200, 200, 200)
        self.active_border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)

    def handle_pygame_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.hitbox.collidepoint(event.pos)

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                self.active = False

            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def update(self, delta, **kwargs):
        pass

    def draw(self, screen):

        pos = self.get_global_position()

        rect = pygame.Rect(pos.x, pos.y, self.size[0], self.size[1])

        pygame.draw.rect(screen, self.bg_color, rect)

        border = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(screen, border, rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (pos.x + 5, pos.y + 5))