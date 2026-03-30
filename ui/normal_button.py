import pygame
from .ui_object import UiObject
from data import Sounds, SoundChannels, PlayerData

class NormalButton(UiObject):
    def __init__(
        self,
        position,
        text,
        font: pygame.font.Font,
        callback=None,
        size = (400, 100),
        color=(60, 60, 60),
        hover_color=(80, 80, 80),
        text_color=(255, 255, 255)
    ):
        super().__init__(position)

        self.size = pygame.Vector2(size)
        self.callback = callback

        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

        self.font = font
        self.text = text

        self._render_text()

    def set_text(self, new_text):
        self.text = new_text
        self._render_text()

    def center_by_x(self, width: int):
        self.position.x = (width - self.size.x) // 2

    def center_by_y(self, height: int):
        self.position.y = (height - self.size.y) // 2

    def _render_text(self):
        self.text_render = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_render.get_rect()

    def get_rect(self):
        return pygame.Rect(self.get_global_position(), self.size)

    def is_mouse_on_button(self):
        return self.get_rect().collidepoint(pygame.mouse.get_pos())

    def handle_pygame_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_mouse_on_button():
                if callable(self.callback):
                    self.callback()
                    Sounds.play_sound(Sounds.BUTTON_PRESS, SoundChannels.SYSTEM, PlayerData.SFX_VOLUME)

    def draw_at(self, screen, position: pygame.Vector2):
        rect = pygame.Rect(position.x, position.y, self.size.x, self.size.y)
        current_color = self.hover_color if rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, current_color, rect)

        self.text_rect.center = rect.center
        screen.blit(self.text_render, self.text_rect)

    def draw(self, screen):
        rect = self.get_rect()
        current_color = self.hover_color if self.is_mouse_on_button() else self.color
        pygame.draw.rect(screen, current_color, rect)

        self.text_rect.center = rect.center
        screen.blit(self.text_render, self.text_rect)
