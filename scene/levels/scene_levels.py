from ..scene_type import SceneType
from ..scene_manager import SceneManager
from ..scene import Scene
from ui import NormalButton, Text, UiManager
from data import Fonts, Levels, const
import pygame


class SceneLevels(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager, SceneType.LEVELS)

        self.ui = UiManager()
        self.level_index = 0

        # =======================
        # TITLE
        # =======================

        self.title = Text(
            pygame.Vector2(0, 40),
            Fonts.LOGO_70,
            "LEVELS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        # =======================
        # LEVEL NAME
        # =======================

        self.level_name = Text(
            pygame.Vector2(0, 200),
            Fonts.NORMAL_30,
            ""
        )
        self.level_name.center_by_x(const.WINDOW_SIZE[0])

        # =======================
        # BUTTONS
        # =======================

        center_x = const.WINDOW_SIZE[0] // 2
        level_y = 200

        btn_prev = NormalButton(
            position=pygame.Vector2(center_x - 200, level_y - 20),
            size=(60, 60),
            text="<",
            font=Fonts.NORMAL_30,
            callback=self._prev_level
        )

        btn_next = NormalButton(
            position=pygame.Vector2(center_x + 140, level_y - 20),
            size=(60, 60),
            text=">",
            font=Fonts.NORMAL_30,
            callback=self._next_level
        )

        btn_play = NormalButton(
            position=pygame.Vector2(0, 320),
            size=(240, 60),
            text="Play",
            font=Fonts.NORMAL_30,
            callback=self._play_level
        )
        btn_play.center_by_x(const.WINDOW_SIZE[0])

        btn_back = NormalButton(
            position=pygame.Vector2(20, 20),
            size=(120, 40),
            text="Back",
            font=Fonts.NORMAL_30,
            callback=self._back_to_menu
        )

        # =======================
        # ADD UI
        # =======================

        self.ui.add_ui_object(self.title)
        self.ui.add_ui_object(self.level_name)
        self.ui.add_ui_object(btn_prev)
        self.ui.add_ui_object(btn_next)
        self.ui.add_ui_object(btn_play)
        self.ui.add_ui_object(btn_back)

        self._update_level_text()

    # =======================
    # LEVEL LOGIC
    # =======================

    @property
    def current_level(self):
        return Levels.ALL_LEVELS[self.level_index]

    def _next_level(self):
        self.level_index += 1
        if self.level_index >= len(Levels.ALL_LEVELS):
            self.level_index = 0
        self._update_level_text()

    def _prev_level(self):
        self.level_index -= 1
        if self.level_index < 0:
            self.level_index = len(Levels.ALL_LEVELS) - 1
        self._update_level_text()

    def _update_level_text(self):
        self.level_name.text = self.current_level.name
        self.level_name.center_by_x(const.WINDOW_SIZE[0])

    def _play_level(self):
        game_scene = self.scene_manager.get_scene(SceneType.GAME)
        game_scene.load_level(self.current_level)
        self.scene_manager.set_scene(SceneType.GAME)

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    # =======================
    # SCENE
    # =======================

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)
        self.ui.draw(screen)
