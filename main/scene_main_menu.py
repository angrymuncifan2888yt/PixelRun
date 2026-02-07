from scene import Scene, SceneType
from ui import UiManager, Text, NormalButton
from data import Fonts, const
from .main_menu_background import MainMenuBackground
import pygame


class SceneMainMenu(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.MAIN_MENU)

        self.ui = UiManager()

        # Фон
        self.ui.add_ui_object(MainMenuBackground())

        # Заголовок
        title = Text(
            pygame.Vector2(0, 80),
            Fonts.LOGO_100,
            "PIXELRUN"
        )
        title.center_by_x(const.WINDOW_SIZE[0])

        # Параметры кнопок
        button_width = 260
        button_height = 60
        start_y = 230
        spacing = 70

        # Skins
        btn_skins = NormalButton(
            position=pygame.Vector2(0, start_y + spacing),
            size=(button_width, button_height),
            text="Skins",
            font=Fonts.NORMAL_30,
            callback=self._button_skins_callback
        )
        btn_skins.center_by_x(const.WINDOW_SIZE[0])

        # Levels
        btn_levels = NormalButton(
            position=pygame.Vector2(0, start_y),
            size=(button_width, button_height),
            text="Play",
            font=Fonts.NORMAL_30,
            callback=self._button_levels_callback
        )
        btn_levels.center_by_x(const.WINDOW_SIZE[0])

        # Editor
        btn_editor = NormalButton(
            position=pygame.Vector2(0, start_y + spacing * 2),
            size=(button_width, button_height),
            text="Editor",
            font=Fonts.NORMAL_30,
            callback=self._button_editor_callback
        )
        btn_editor.center_by_x(const.WINDOW_SIZE[0])

        # Exit
        btn_exit = NormalButton(
            position=pygame.Vector2(0, start_y + spacing * 3),
            size=(button_width, button_height),
            text="Exit",
            font=Fonts.NORMAL_30,
            callback=self._button_exit_callback
        )
        btn_exit.center_by_x(const.WINDOW_SIZE[0])

        self.ui.add_ui_object(title)
        self.ui.add_ui_object(btn_skins)
        self.ui.add_ui_object(btn_levels)
        self.ui.add_ui_object(btn_editor)
        self.ui.add_ui_object(btn_exit)

    def _button_skins_callback(self):
        self.scene_manager.set_scene(SceneType.SKINS)

    def _button_levels_callback(self):
        self.scene_manager.set_scene(SceneType.LEVELS)

    def _button_editor_callback(self):
        self.scene_manager.set_scene(SceneType.EDITOR)
        
    def _button_exit_callback(self):
        pygame.quit()
        raise SystemExit

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)
        self.ui.draw(screen)
