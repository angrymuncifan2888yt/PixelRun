from ..scene import Scene
from ..scene_type import SceneType
from ui import UiManager, Text, NormalButton
from data import FontStorage, const
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
            FontStorage.LOGO_100,
            "PIXELRUN"
        )
        title.center_by_x(const.WINDOW_SIZE[0])

        # Параметры кнопок
        button_width = 260
        button_height = 60
        start_y = 230
        spacing = 70

        # Play
        btn_play = NormalButton(
            position=pygame.Vector2(0, start_y),
            size=(button_width, button_height),
            text="Play",
            font=FontStorage.NORMAL_30,
            callback=self._button_play_callback
        )
        btn_play.center_by_x(const.WINDOW_SIZE[0])

        # Skins
        btn_skins = NormalButton(
            position=pygame.Vector2(0, start_y + spacing),
            size=(button_width, button_height),
            text="Skins",
            font=FontStorage.NORMAL_30,
            callback=self._button_skins_callback
        )
        btn_skins.center_by_x(const.WINDOW_SIZE[0])

        # Levels
        btn_levels = NormalButton(
            position=pygame.Vector2(0, start_y + spacing * 2),
            size=(button_width, button_height),
            text="Levels",
            font=FontStorage.NORMAL_30,
            callback=self._button_levels_callback
        )
        btn_levels.center_by_x(const.WINDOW_SIZE[0])

        # Exit
        btn_exit = NormalButton(
            position=pygame.Vector2(0, start_y + spacing * 3),
            size=(button_width, button_height),
            text="Exit",
            font=FontStorage.NORMAL_30,
            callback=self._button_exit_callback
        )
        btn_exit.center_by_x(const.WINDOW_SIZE[0])

        self.ui.add_ui_object(title)
        self.ui.add_ui_object(btn_play)
        self.ui.add_ui_object(btn_skins)
        self.ui.add_ui_object(btn_levels)
        self.ui.add_ui_object(btn_exit)

    def _button_play_callback(self):
        self.scene_manager.set_scene(SceneType.GAME)

    def _button_skins_callback(self):
        self.scene_manager.set_scene(SceneType.SKINS)

    def _button_levels_callback(self):
        self.scene_manager.set_scene(SceneType.LEVELS)

    def _button_exit_callback(self):
        pygame.quit()
        raise SystemExit

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._button_play_callback()

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)
        self.ui.draw(screen)
