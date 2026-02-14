from typing import Any
from .entity_panel import EntityPanel
from scene import Scene, SceneType
from ui import NormalButton, UiManager, Text
import pygame
from util import Camera
from core import World, Platform, Spike, Trigger
from core.render import render_entity, render_hitbox
from data import const, Fonts
from level import Level, Deserializator, Serializator


class SceneEditor(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.EDITOR)

        # <-- UI -->
        self.ui = UiManager()

        # Кнопка Back
        btn_back = NormalButton(
            position=pygame.Vector2(10, 20),
            size=(120, 40),
            text="Back",
            font=Fonts.NORMAL_30,
            callback=self._back_to_menu
        )

        # Кнопка Copy
        btn_copy = NormalButton(
            position=pygame.Vector2(const.WINDOW_SIZE[0] - 110, 10),
            size=(100, 100),
            text="Copy",
            font=Fonts.NORMAL_30,
            callback=None
        )
        # Кнопка Paste
        btn_paste = NormalButton(
            position=pygame.Vector2(const.WINDOW_SIZE[0] - 220, 10),
            size=(100, 100),
            text="Paste",
            font=Fonts.NORMAL_30,
            callback=None
        )
        # Кнопка Edit
        btn_edit = NormalButton(
            position=pygame.Vector2(const.WINDOW_SIZE[0] - 220, 120),
            size=(100, 100),
            text="Edit",
            font=Fonts.NORMAL_30,
            callback=None
        )        
        # Кнопка Delete
        btn_delete = NormalButton(
            position=pygame.Vector2(const.WINDOW_SIZE[0] - 110, 120),
            size=(100, 100),
            text="Delete",
            font=Fonts.NORMAL_30,
            callback=None
        )
        # Кнопка Edit Special
        btn_edit_special = NormalButton(
            position=pygame.Vector2(const.WINDOW_SIZE[0] - 220, 230),
            size=(210, 100),
            text="Edit Special",
            font=Fonts.NORMAL_30,
            callback=None
        )        
        # Кнопка Edit level
        btn_edit_level = NormalButton(
            position=pygame.Vector2(0, 10),
            size=(260, 60),
            text="Edit Level",
            font=Fonts.NORMAL_30,
            callback=None
        )        
        btn_edit_level.center_by_x(const.WINDOW_SIZE[0])

        # Кнопка Play
        btn_play = NormalButton(
            position=pygame.Vector2(10, const.WINDOW_SIZE[1] - 330),
            size=(100, 100),
            text="Play",
            font=Fonts.NORMAL_30,
            callback=None
        )    
        # Кнопка Save
        btn_save = NormalButton(
            position=pygame.Vector2(10, const.WINDOW_SIZE[1] - 220),
            size=(100, 100),
            text="Save",
            font=Fonts.NORMAL_30,
            callback=None
        )
        # Кнопка Load
        btn_load = NormalButton(
            position=pygame.Vector2(10, const.WINDOW_SIZE[1] - 110),
            size=(100, 100),
            text="Load",
            font=Fonts.NORMAL_30,
            callback=None
        )
        # Кнопка Hitbox
        btn_hitbox = NormalButton(
            position=pygame.Vector2(const.WINDOW_SIZE[0] - 110, const.WINDOW_SIZE[1] - 110),
            size=(100, 100),
            text="Hitbox",
            font=Fonts.NORMAL_30,
            callback=self._button_hitbox_callback
        )

        self.entity_panel = EntityPanel(
            position=pygame.Vector2(10, 70),
            width=240,
            height=500
        )
    
        self.ui.add_ui_object(btn_hitbox)
        self.ui.add_ui_object(btn_back)
        self.ui.add_ui_object(btn_copy)
        self.ui.add_ui_object(btn_paste)
        self.ui.add_ui_object(btn_delete)
        self.ui.add_ui_object(btn_edit)
        self.ui.add_ui_object(btn_edit_level)
        self.ui.add_ui_object(btn_save)
        self.ui.add_ui_object(btn_load)
        self.ui.add_ui_object(btn_edit_special)
        self.ui.add_ui_object(btn_play)
        self.ui.add_ui_object(self.entity_panel)
        # <-- /UI -->

        # <-- LEVEL -->
        self.level = Level()
        self.world = World()
        self.show_hitboxes = False
        self.camera = Camera(pygame.Vector2(0, 0), *const.WINDOW_SIZE)
        # Test
        self.world.add_entity(Platform(self.world, pygame.Vector2(0, 0)))
        self.world.add_entity(Spike(self.world, pygame.Vector2(300, 300)))
        # <-- /LEVEL -->

    def _draw_world(self, screen):
        # Grid
        grid_size = 50
        grid_color = (60, 60, 60)

        start_x = int(self.camera.position.x // grid_size * grid_size)
        end_x = int(self.camera.position.x + self.camera.width)

        start_y = int(self.camera.position.y // grid_size * grid_size)
        end_y = int(self.camera.position.y + self.camera.height)

        for x in range(start_x, end_x, grid_size):
            screen_x = x - self.camera.position.x
            pygame.draw.line(
                screen,
                grid_color,
                (screen_x, 0),
                (screen_x, self.camera.height)
            )

        for y in range(start_y, end_y, grid_size):
            screen_y = y - self.camera.position.y
            pygame.draw.line(
                screen,
                grid_color,
                (0, screen_y),
                (self.camera.width, screen_y)
            )

        # world
        entities = self.world.get_nearest_entities(self.camera.position, 2000)
        for entity in entities:
            if self.camera.is_object_visible(entity.position, entity.width, entity.height):
                if isinstance(entity, Trigger):
                    old_opacity = entity.opacity
                    entity.opacity = 255  # Сделаем триггеры полностью видимыми для удобства редактирования
                    render_entity(screen, entity, self.camera)
                    entity.opacity = old_opacity  # Вернем обратно
                else:
                    render_entity(screen, entity, self.camera)
                if self.show_hitboxes:
                    render_hitbox(screen, entity.hitbox, self.camera)

    # buttons
    def _button_hitbox_callback(self):
        self.show_hitboxes = not self.show_hitboxes
    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    # interact
    def _left_click(self, event):
        selected_cls = self.entity_panel.get_selected()
        if not selected_cls:
            return

        mouse_screen = pygame.Vector2(event.pos)

        # Проверяем что клик не по UI
        if self.ui.is_mouse_over_ui(mouse_screen):
            return

        # Переводим в world координаты
        mouse_world = mouse_screen + self.camera.position

        # Привязка к сетке (очень важно для редактора)
        grid_size = 50
        mouse_world.x = int(mouse_world.x // grid_size) * grid_size
        mouse_world.y = int(mouse_world.y // grid_size) * grid_size

        # Создаем объект
        entity = selected_cls(self.world, mouse_world)
        self.world.add_entity(entity)

    def _right_click(self, event):
        print("del")
    # Scene methods
    def handle_pygame_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            self._left_click(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Правая кнопка мыши
            self._right_click(event)

        self.ui.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        # World
        self.world.update_all_hitboxes()

        # ui
        self.ui.update(delta, **kwargs)

        # camera movement
        camera_speed = 1000
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.position.y -= camera_speed * delta
        if keys[pygame.K_s]:
            self.camera.position.y += camera_speed * delta
        if keys[pygame.K_a]:
            self.camera.position.x -= camera_speed * delta
        if keys[pygame.K_d]:
            self.camera.position.x += camera_speed * delta

    def draw(self, screen):
        screen.fill(self.level.background_color)
        self._draw_world(screen)
        self.ui.draw(screen)