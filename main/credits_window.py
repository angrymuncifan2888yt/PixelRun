import pygame
from ui import NormalButton, Text
from ui.ui_manager import UiManager
from data import Fonts, const
from window import Window, WindowType


WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750


class CreditsWindow(Window):

    def __init__(self, manager):
        super().__init__(manager, WindowType.CREDITS)
        text = """
Game by Angry Muni 

Skins textures by: RobTopGames

Portals, orbs, triggers,
checkpoint textures by RobTopGames

Background music: Me Time by Avanti

Inspired by Geometry Dash by RobTopGames
"""
        self.ui = UiManager()

        self.rect = pygame.Rect(
            const.WINDOW_SIZE[0] // 2 - WINDOW_WIDTH // 2,
            const.WINDOW_SIZE[1] // 2 - WINDOW_HEIGHT // 2,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        # 🔹 Заголовок
        self.title = Text(
            pygame.Vector2(0, self.rect.y + 40),
            Fonts.NORMAL_40,
            "CREDITS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        # =========================
        # 🟢 ТЕКСТ КРЕДИТОВ
        # =========================
        self.text_objects = []

        start_y = self.rect.y + 120
        line_spacing = 40

        lines = text.split("\n")

        for i, line in enumerate(lines):
            txt = Text(
                pygame.Vector2(0, start_y + i * line_spacing),
                Fonts.NORMAL_30,
                line
            )
            txt.center_by_x(const.WINDOW_SIZE[0])
            self.text_objects.append(txt)

        # =========================
        # 🟢 КНОПКА ЗАКРЫТИЯ
        # =========================
        self.btn_close = NormalButton(
            position=pygame.Vector2(self.rect.centerx - 100, self.rect.bottom - 90),
            size=(200, 55),
            text="Close",
            font=Fonts.NORMAL_30,
            callback=self.close
        )

        # =========================
        # 🟢 ADD UI
        # =========================
        self.ui.add_ui_object(self.title)

        for txt in self.text_objects:
            self.ui.add_ui_object(txt)

        self.ui.add_ui_object(self.btn_close)

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta_time):
        self.ui.update(delta_time)

    def draw(self, screen):
        overlay = pygame.Surface(const.WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        self.ui.draw(screen)