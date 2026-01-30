from ..scene_type import SceneType
from ..scene_manager import SceneManager
from ..scene import Scene
from ui import NormalButton, Text, UiManager
from data import FontStorage, levels, const
import pygame


class SceneLevels(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager, SceneType.LEVELS)

        self.ui = UiManager()
        # Заголовок
        self.title = Text(
            pygame.Vector2(0, 40),
            FontStorage.LOGO_70,
            "LEVELS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        # Кнопка Back
        btn_back = NormalButton(
            position=pygame.Vector2(20, 20),
            size=(120, 40),
            text="Back",
            font=FontStorage.NORMAL_30,
            callback=self._back_to_menu
        )

        self.ui.add_ui_object(self.title)
        self.ui.add_ui_object(btn_back)

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta, **kwargs)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)
        self.ui.draw(screen)
