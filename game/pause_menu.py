from ui import UiObject, UiManager, Text, NormalButton
from data import Fonts
import pygame


class PauseMenu(UiObject):
    def __init__(self, position, screen_size, on_resume=None, on_menu=None, on_reset=None):
        super().__init__(position)

        self.ui = UiManager()

        self.screen_size = screen_size
        self.on_resume = on_resume
        self.on_menu = on_menu
        self.on_reset = on_reset

        self._build_ui()

    def _build_ui(self):
        w, h = self.screen_size

        # затемнённый фон
        self.background = UiObject((0, 0))
        self.background.draw = self._draw_background

        # заголовок
        title = Text(
            position=(0, 60),
            font=Fonts.LOGO_100,
            text="PAUSE",
            color=(255, 255, 255)
        )
        title.center_by_x(w)

        # кнопки
        btn_resume = NormalButton(
            position=(0, 0),
            size=(260, 60),
            text="Continue",
            font=Fonts.NORMAL_30,
            callback=self._resume,
            color=(70, 70, 70),
            hover_color=(120, 120, 120)
        )

        btn_reset = NormalButton(
            position=(0, 0),
            size=(260, 60),
            text="Reset",
            font=Fonts.NORMAL_30,
            callback=self._reset,
            color=(70, 70, 70),
            hover_color=(120, 120, 120)
        )

        btn_menu = NormalButton(
            position=(0, 0),
            size=(260, 60),
            text="Main Menu",
            font=Fonts.NORMAL_30,
            callback=self._menu,
            color=(70, 70, 70),
            hover_color=(120, 120, 120)
        )

        btn_resume.center_by_x(w)
        btn_reset.center_by_x(w)
        btn_menu.center_by_x(w)

        btn_resume.position.y = h // 2 - 40
        btn_reset.position.y = h // 2 + 40
        btn_menu.position.y = h // 2 + 120

        # добавление в менеджер
        self.ui.add_ui_object(self.background)
        self.ui.add_ui_object(title)
        self.ui.add_ui_object(btn_resume)
        self.ui.add_ui_object(btn_reset)
        self.ui.add_ui_object(btn_menu)

    def _draw_background(self, screen):
        s = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        screen.blit(s, (0, 0))

    def _resume(self):
        if callable(self.on_resume):
            self.on_resume()

    def _menu(self):
        if callable(self.on_menu):
            self.on_menu()

    def _reset(self):
        if callable(self.on_reset):
            self.on_reset()

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        self.ui.draw(screen)
