from scene import Scene, SceneType, SceneManager
from ui import NormalButton, Text, UiManager
from data import Fonts, Levels, const
from util import open_file_dialog
from level import Validator
import pygame


class SceneLevels(Scene):

    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager, SceneType.LEVELS)

        self.ui = UiManager()
        self.level_index = 0

        self.title = Text(
            pygame.Vector2(0, 40),
            Fonts.LOGO_70,
            "LEVELS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        self.level_name = Text(
            pygame.Vector2(0, 200),
            Fonts.NORMAL_30,
            ""
        )
        self.level_name.center_by_x(const.WINDOW_SIZE[0])

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

        btn_load_custom = NormalButton(
            position=pygame.Vector2(0, 400),
            size=(320, 60),
            text="Load Custom Level",
            font=Fonts.NORMAL_30,
            callback=self._load_custom_level
        )
        btn_load_custom.center_by_x(const.WINDOW_SIZE[0])

        btn_remove = NormalButton(
            position=pygame.Vector2(0, 480),
            size=(320, 60),
            text="Remove Level",
            font=Fonts.NORMAL_30,
            callback=self._button_remove_callback
        )
        btn_remove.center_by_x(const.WINDOW_SIZE[0])

        btn_back = NormalButton(
            position=pygame.Vector2(20, 20),
            size=(120, 40),
            text="Back",
            font=Fonts.NORMAL_30,
            callback=self._back_to_menu
        )

        self.ui.add_ui_object(self.title)
        self.ui.add_ui_object(self.level_name)
        self.ui.add_ui_object(btn_prev)
        self.ui.add_ui_object(btn_next)
        self.ui.add_ui_object(btn_play)
        self.ui.add_ui_object(btn_load_custom)
        self.ui.add_ui_object(btn_back)
        self.ui.add_ui_object(btn_remove)

        self._update_level_text()

    @property
    def current_level(self):
        if not Levels.ALL_LEVELS:
            return None
        return Levels.ALL_LEVELS[self.level_index]

    def _next_level(self):
        if not Levels.ALL_LEVELS:
            return

        self.level_index += 1
        if self.level_index >= len(Levels.ALL_LEVELS):
            self.level_index = 0

        self._update_level_text()

    def _prev_level(self):
        if not Levels.ALL_LEVELS:
            return

        self.level_index -= 1
        if self.level_index < 0:
            self.level_index = len(Levels.ALL_LEVELS) - 1

        self._update_level_text()

    def _update_level_text(self):
        if not Levels.ALL_LEVELS:
            self.level_name.text = "No Levels"
        else:
            if self.level_index >= len(Levels.ALL_LEVELS):
                self.level_index = 0

            self.level_name.text = self.current_level.name

        self.level_name.center_by_x(const.WINDOW_SIZE[0])

    def _play_level(self):
        if not self.current_level:
            return

        game_scene = self.scene_manager.get_scene(SceneType.GAME)
        game_scene.load_level(self.current_level)
        self.scene_manager.set_scene(SceneType.GAME)

    def _button_remove_callback(self):
        if not self.current_level:
            return

        try:
            Levels.ALL_LEVELS.remove(self.current_level)

            if self.level_index >= len(Levels.ALL_LEVELS):
                self.level_index = max(0, len(Levels.ALL_LEVELS) - 1)

            self._update_level_text()

        except:
            pass

    def _load_custom_level(self):
        path = open_file_dialog(
            title="Select level file",
            filetypes=[("Level files", "*.json")]
        )

        if path:
            try:
                level = Levels.load_level_from_file(path)

                if Validator.is_level_valid(level):
                    Levels.ALL_LEVELS.append(level)
                    self.level_index = len(Levels.ALL_LEVELS) - 1
                    self._update_level_text()

            except:
                pass

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)
        self.ui.draw(screen)