import pygame
from ui import NormalButton, LineEdit
from ui.ui_manager import UiManager
from data import Fonts, const, Settings
from window import Window, WindowType


WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750


class SettingsWindow(Window):

    def __init__(self, manager, ):
        super().__init__(manager, WindowType.SETTINGS)

        self.ui = UiManager()

        self.rect = pygame.Rect(
            const.WINDOW_SIZE[0] // 2 - WINDOW_WIDTH // 2,
            const.WINDOW_SIZE[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        button_y = self.rect.bottom - 90

        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.right - 240, button_y),
            size=(200, 55),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

        self.ui.add_ui_object(self.btn_close)

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)
    def update(self, delta_time):
        self.ui.update(delta_time)
    def draw(self, screen):
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)
        self.ui.draw(screen)
        