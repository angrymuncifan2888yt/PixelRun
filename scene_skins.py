from scene import Scene, SceneType
from ui import UiManager, Text, NormalButton
from data import Fonts, const, Skins
import pygame


class SceneSkins(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager, SceneType.SKINS)

        self.ui = UiManager()

        # Индекс выбранного скина
        self.skin_index = 0
        # Какой скин применён (Applied)
        self.applied_skin = None

        # Флаг отложенной инициализации (для того, чтобы SceneGame уже существовала)
        self.initialized_from_game = False

        # Анимация скинов
        self.anim_index = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.12

        # =======================
        # UI
        # =======================
        self._setup_ui()
        self._update_skin_text()

    # -----------------------
    # UI Инициализация
    # -----------------------
    def _setup_ui(self):
        # Заголовок
        self.title = Text(
            pygame.Vector2(0, 40),
            Fonts.LOGO_70,
            "SKINS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        # Название скина
        self.skin_name = Text(
            pygame.Vector2(0, 140),
            Fonts.NORMAL_30,
            ""
        )
        self.skin_name.center_by_x(const.WINDOW_SIZE[0])

        # Описание скина
        self.skin_description = Text(
            pygame.Vector2(0, 340),
            Fonts.NORMAL_25,
            ""
        )
        self.skin_description.center_by_x(const.WINDOW_SIZE[0])

        center_x = const.WINDOW_SIZE[0] // 2
        preview_y = 260

        # Кнопка "<"
        btn_prev = NormalButton(
            position=pygame.Vector2(center_x - 160, preview_y - 30),
            size=(60, 60),
            text="<",
            font=Fonts.NORMAL_30,
            callback=self._prev_skin
        )

        # Кнопка ">"
        btn_next = NormalButton(
            position=pygame.Vector2(center_x + 100, preview_y - 30),
            size=(60, 60),
            text=">",
            font=Fonts.NORMAL_30,
            callback=self._next_skin
        )

        # Кнопка Apply
        self.btn_apply = NormalButton(
            position=pygame.Vector2(0, 420),
            size=(220, 60),
            text="Apply",
            font=Fonts.NORMAL_30,
            callback=self._apply_skin
        )
        self.btn_apply.center_by_x(const.WINDOW_SIZE[0])

        # Кнопка Back
        btn_back = NormalButton(
            position=pygame.Vector2(20, 20),
            size=(120, 40),
            text="Back",
            font=Fonts.NORMAL_30,
            callback=self._back_to_menu
        )

        # Добавляем в UiManager
        self.ui.add_ui_object(self.title)
        self.ui.add_ui_object(self.skin_name)
        self.ui.add_ui_object(self.skin_description)
        self.ui.add_ui_object(btn_prev)
        self.ui.add_ui_object(btn_next)
        self.ui.add_ui_object(self.btn_apply)
        self.ui.add_ui_object(btn_back)

    # =======================
    # Логика скинов
    # =======================

    @property
    def current_skin(self):
        return Skins.ALL_SKINS[self.skin_index]

    def _next_skin(self):
        self.skin_index += 1
        if self.skin_index >= len(Skins.ALL_SKINS):
            self.skin_index = 0
        self._update_skin_text()

    def _prev_skin(self):
        self.skin_index -= 1
        if self.skin_index < 0:
            self.skin_index = len(Skins.ALL_SKINS) - 1
        self._update_skin_text()

    def _update_skin_text(self):
        skin = self.current_skin
        self.skin_name.text = skin.name
        self.skin_name.center_by_x(const.WINDOW_SIZE[0])
        self.skin_description.text = skin.description
        self.skin_description.center_by_x(const.WINDOW_SIZE[0])

        self.anim_index = 0
        self.anim_timer = 0.0

        self._update_apply_button()

    def _update_apply_button(self):
        if self.applied_skin == self.current_skin:
            self.btn_apply.set_text("Applied")
        else:
            self.btn_apply.set_text("Apply")

    def _apply_skin(self):
        game_scene = self.scene_manager.get_scene(SceneType.GAME)
        if game_scene:
            game_scene.set_skin(self.current_skin)
            self.applied_skin = self.current_skin
            self._update_apply_button()

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    # =======================
    # SCENE METHODS
    # =======================

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        # -----------------------
        # Отложенная инициализация из SceneGame
        # -----------------------
        if not self.initialized_from_game:
            game_scene = self.scene_manager.get_scene(SceneType.GAME)
            if game_scene:
                current_skin = game_scene.player.skin
                try:
                    self.skin_index = Skins.ALL_SKINS.index(current_skin)
                except ValueError:
                    self.skin_index = 0
                self.applied_skin = current_skin
                self._update_skin_text()
                self.initialized_from_game = True

        # Анимация скина
        skin = self.current_skin
        if skin.animations:
            self.anim_timer += delta
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.anim_index += 1
                if self.anim_index >= len(skin.animations):
                    self.anim_index = 0

        self.ui.update(delta)

    def draw(self, screen):
        screen.fill(const.WINDOW_BACKGROUND_COLOR)

        self.ui.draw(screen)

        # Рисуем анимацию скина
        skin = self.current_skin
        sprite = skin.animations[self.anim_index] if skin.animations else skin.standing_sprite

        rect = sprite.get_rect()
        rect.center = (const.WINDOW_SIZE[0] // 2, 260)
        screen.blit(sprite, rect)
