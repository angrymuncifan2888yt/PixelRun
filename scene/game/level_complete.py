from ui import UiObject, UiManager, Text, NormalButton
from data import FontStorage
import pygame


class LevelCompleteMenu(UiObject):
    def __init__(self, position, screen_size, on_play_again=None, on_menu=None):
        super().__init__(position)

        self.ui = UiManager()
        self.screen_size = screen_size
        self.on_play_again = on_play_again
        self.on_menu = on_menu

        self._build_ui()

    def _build_ui(self):
        w, h = self.screen_size

        # затемнённый фон
        self.background = UiObject((0, 0))
        self.background.draw = self._draw_background

        # заголовок
        title = Text(
            position=(0, 60),
            font=FontStorage.LOGO_100,
            text="LEVEL COMPLETE!",
            color=(255, 255, 255)
        )
        title.center_by_x(w)

        # кнопки
        btn_play_again = NormalButton(
            position=(0, 0),
            size=(260, 60),
            text="Play Again",
            font=FontStorage.NORMAL_30,
            callback=self._play_again,
            color=(70, 70, 70),
            hover_color=(120, 120, 120)
        )

        btn_menu = NormalButton(
            position=(0, 0),
            size=(260, 60),
            text="Main Menu",
            font=FontStorage.NORMAL_30,
            callback=self._menu,
            color=(70, 70, 70),
            hover_color=(120, 120, 120)
        )

        btn_play_again.center_by_x(w)
        btn_menu.center_by_x(w)

        # вертикальное расположение кнопок
        btn_play_again.position.y = h // 2 - 40
        btn_menu.position.y = h // 2 + 40

        # добавление в UiManager
        self.ui.add_ui_object(self.background)
        self.ui.add_ui_object(title)
        self.ui.add_ui_object(btn_play_again)
        self.ui.add_ui_object(btn_menu)

    def _draw_background(self, screen):
        s = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))  # полупрозрачный чёрный
        screen.blit(s, (0, 0))

    def _play_again(self):
        if callable(self.on_play_again):
            self.on_play_again()

    def _menu(self):
        if callable(self.on_menu):
            self.on_menu()

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        self.ui.draw(screen)
