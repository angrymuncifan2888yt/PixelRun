import pygame
from scene import Scene, SceneType
from ui import UiManager, Text, NormalButton, TabContainer
from data import Fonts, const, Skins, PlayerData


class SceneSkins(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager, SceneType.SKINS)

        self.ui = UiManager()

        self.cube_index = 0
        self.ufo_index = 0

        self.current_tab = 0

        self._setup_ui()
        self._update_skin_text()

    def _setup_ui(self):
        self.title = Text(
            pygame.Vector2(0, 40),
            Fonts.LOGO_70,
            "SKINS"
        )
        self.title.center_by_x(const.WINDOW_SIZE[0])

        self.skin_name = Text(
            pygame.Vector2(0, 140),
            Fonts.NORMAL_30,
            ""
        )

        self.skin_description = Text(
            pygame.Vector2(0, 340),
            Fonts.NORMAL_25,
            ""
        )

        center_x = const.WINDOW_SIZE[0] // 2
        preview_y = 260

        btn_prev = NormalButton(
            pygame.Vector2(center_x - 160, preview_y - 30),
            "<",
            size=(60, 60),
            font=Fonts.NORMAL_30,
            callback=self._prev_skin
        )

        btn_next = NormalButton(
            pygame.Vector2(center_x + 100, preview_y - 30),
            ">",
            size=(60, 60),
            font=Fonts.NORMAL_30,
            callback=self._next_skin
        )

        self.btn_apply = NormalButton(
            pygame.Vector2(0, 420),
            size=(220, 60),
            text="Apply",
            font=Fonts.NORMAL_30,
            callback=self._apply_skin
        )
        self.btn_apply.center_by_x(const.WINDOW_SIZE[0])

        btn_back = NormalButton(
            pygame.Vector2(20, 20),
            size=(120, 40),
            text="Back",
            font=Fonts.NORMAL_30,
            callback=self._back_to_menu
        )

        tab_y = 80

        self.btn_cube_tab = NormalButton(
            pygame.Vector2(0, tab_y),
            size=(150, 40),
            text="Cube",
            font=Fonts.NORMAL_25,
            callback=lambda: self._switch_tab(0)
        )

        self.btn_ufo_tab = NormalButton(
            pygame.Vector2(170, tab_y),
            size=(150, 40),
            text="UFO",
            font=Fonts.NORMAL_25,
            callback=lambda: self._switch_tab(1)
        )

        self.btn_cube_tab.center_by_x(const.WINDOW_SIZE[0] // 2 - 250)
        self.btn_ufo_tab.center_by_x(const.WINDOW_SIZE[0] // 2 + 100)

        self.tabs = TabContainer(
            pygame.Vector2(0, 0),
            (const.WINDOW_SIZE[0], const.WINDOW_SIZE[1])
        )

        self.tabs.add_tab([
            self.title,
            self.skin_name,
            self.skin_description,
            btn_prev,
            btn_next,
            self.btn_apply,
            btn_back,
        ])

        self.tabs.add_tab([
            self.title,
            self.skin_name,
            self.skin_description,
            btn_prev,
            btn_next,
            self.btn_apply,
            btn_back,
        ])

        for obj in [self.tabs]:
            self.ui.add_ui_object(obj)
            self.ui.add_ui_object(self.btn_cube_tab)
            self.ui.add_ui_object(self.btn_ufo_tab)
        self._update_tab_buttons()

    @property
    def current_skin(self):
        if self.current_tab == 0:
            return Skins.CUBE_SKINS[self.cube_index]
        return Skins.UFO_SKINS[self.ufo_index]

    def _update_tab_buttons(self):
        if self.current_tab == 0:
            self.btn_cube_tab.color = (0, 200, 0)   # зелёный
            self.btn_ufo_tab.color = (60, 60, 60)   # обычный
            self.btn_ufo_tab.hover_color = (80, 80, 80)
            self.btn_cube_tab.hover_color = (0, 200, 0)
        else:
            self.btn_cube_tab.color = (60, 60, 60)
            self.btn_cube_tab.hover_color = (80, 80, 80)
            self.btn_ufo_tab.color = (0, 200, 0)
            self.btn_ufo_tab.hover_color = (0, 200, 0)

    def _switch_tab(self, tab_index):
        self.current_tab = tab_index
        self._update_skin_text()
        self._update_tab_buttons()

    def _next_skin(self):
        if self.current_tab == 0:
            self.cube_index = (self.cube_index + 1) % len(Skins.CUBE_SKINS)
        else:
            self.ufo_index = (self.ufo_index + 1) % len(Skins.UFO_SKINS)

        self._update_skin_text()

    def _prev_skin(self):
        if self.current_tab == 0:
            self.cube_index = (self.cube_index - 1) % len(Skins.CUBE_SKINS)
        else:
            self.ufo_index = (self.ufo_index - 1) % len(Skins.UFO_SKINS)

        self._update_skin_text()

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    def _update_skin_text(self):
        skin = self.current_skin

        self.skin_name.text = skin.name
        self.skin_name.center_by_x(const.WINDOW_SIZE[0])

        self.skin_description.text = skin.description
        self.skin_description.center_by_x(const.WINDOW_SIZE[0])

        self._update_apply_button()

    def _update_apply_button(self):
        current = self.current_skin

        if self.current_tab == 0:
            self.btn_apply.set_text("Applied" if PlayerData.CUBE_SKIN == current else "Apply")
        else:
            self.btn_apply.set_text("Applied" if PlayerData.UFO_SKIN == current else "Apply")

    def _apply_skin_to_all_players(self):
        game_scene = self.scene_manager.get_scene(SceneType.GAME)
        if game_scene:
            if self.current_tab == 0: game_scene.player.cube_skin = self.current_skin
            else: game_scene.player.ufo_skin = self.current_skin

        main_menu_scene = self.scene_manager.get_scene(SceneType.MAIN_MENU)
        if main_menu_scene:
            if self.current_tab == 0: main_menu_scene.bg.player.cube_skin = self.current_skin
            else: main_menu_scene.bg.player.ufo_skin = self.current_skin

        editor_playtest_scene = self.scene_manager.get_scene(SceneType.EDITOR_PLAYTEST)
        if editor_playtest_scene:
            if self.current_tab == 0: editor_playtest_scene.player.cube_skin = self.current_skin
            else: editor_playtest_scene.player.ufo_skin = self.current_skin

    def _apply_skin(self):
        skin = self.current_skin

        if self.current_tab == 0:
            PlayerData.CUBE_SKIN = skin
        else:
            PlayerData.UFO_SKIN = skin

        PlayerData.save()
        self._update_apply_button()
        self._apply_skin_to_all_players()

    def handle_pygame_event(self, event):
        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        self.ui.update(delta)

    def draw(self, screen):
        screen.fill(PlayerData.WINDOW_BACKGROUND_COLOR)

        self.ui.draw(screen)

        skin = self.current_skin
        sprite = skin.sprite

        width, height = skin.size

        scaled_sprite = pygame.transform.scale(sprite, (width, height))

        rect = scaled_sprite.get_rect()
        rect.center = (const.WINDOW_SIZE[0] // 2, 260)

        screen.blit(scaled_sprite, rect)