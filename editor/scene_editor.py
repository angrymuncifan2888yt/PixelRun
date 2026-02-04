from typing import Any
from scene import Scene, SceneType
from ui import NormalButton, UiManager, Text
import pygame
from data import const, Fonts


class SceneEditor(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.EDITOR)

        self.ui = UiManager()

        # Заголовок
        title = Text(
            pygame.Vector2(0, 80),
            Fonts.LOGO_100,
            "COMING SOON..."
        )
        title.center_by_x(const.WINDOW_SIZE[0])
        title.center_by_y(const.WINDOW_SIZE[1])

        # Кнопка Back
        btn_back = NormalButton(
            position=pygame.Vector2(20, 20),
            size=(120, 40),
            text="Back",
            font=Fonts.NORMAL_30,
            callback=self._back_to_menu
        )

        self.ui.add_ui_object(btn_back)
        self.ui.add_ui_object(title)
    
    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta, **kwargs)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)
        self.ui.draw(screen)