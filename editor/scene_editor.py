from typing import Any
from .entity_panel import EntityPanel
from scene import Scene, SceneType
from ui import NormalButton, UiManager, Text
import pygame
from util import Camera, save_file_dialog, open_file_dialog
from core import World, Platform, Spike, Trigger
from core.render import render_entity, render_hitbox
from data import const, Fonts
from level import Level, Deserializator, Serializator, ENTITY_FACTORY
from .edit_level_window import LevelEditWindow
from .edit_entity_window import EditEntityWindow
from window import WindowManager, WindowType
from .scene_editor_buttons import *
import json
from .scene_editor_ui import create_ui


class SceneEditor(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.EDITOR)

        # <-- UI -->
        create_ui(self)
        # <-- /UI -->

        # <-- LEVEL -->
        self.level = Level()
        self.level_path = None
        self.world = World()
        self.show_hitboxes = False
        self.camera = Camera(pygame.Vector2(0, 0), *const.WINDOW_SIZE)
        self.selected_entities = []
        self.entity_buffer = None  # Для Copy/Paste
        self.use_grid = True
        self.dragging_entity = None
        self.drag_offset = pygame.Vector2(0, 0)

        # Test
        self.world.add_entity(Platform(self.world, pygame.Vector2(0, 0)))
        self.world.add_entity(Spike(self.world, pygame.Vector2(300, 300)))
        # <-- /LEVEL -->

        # <-- WINDOWS -->
        self.window_manager = WindowManager()
        self.level_edit_window = LevelEditWindow(self.window_manager, self.level, const.WINDOW_SIZE)
        self.entity_edit_window = EditEntityWindow(self.window_manager, self.selected_entities, const.WINDOW_SIZE)
        self.window_manager.add_window(self.level_edit_window)
        self.window_manager.add_window(self.entity_edit_window)
        # <-- /WINDOWS -->

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

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

                # Подсветка выбранной сущности
                if entity in self.selected_entities:
                    screen_rect = pygame.Rect(
                        entity.position.x - self.camera.position.x,
                        entity.position.y - self.camera.position.y,
                        entity.width,
                        entity.height
                    )

                    pygame.draw.rect(
                        screen,
                        (0, 255, 0),
                        screen_rect,
                        3
                    )

    # Updates level (for save/play test)
    def _form_level(self):
        # obj
        objects = []
        for entity in self.world.entities:
            objects.append(Serializator.get_entity_json(entity))
        self.level.objects = objects

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

        # Привязка к сетке
        if self.use_grid:
            grid_size = 50
            mouse_world.x = int(mouse_world.x // grid_size) * grid_size
            mouse_world.y = int(mouse_world.y // grid_size) * grid_size

        # Создаем объект
        entity = selected_cls(self.world, mouse_world)
        self.world.add_entity(entity)

    def _right_click(self, event):
        mouse_screen = pygame.Vector2(event.pos)

        if self.ui.is_mouse_over_ui(mouse_screen):
            return

        mouse_world = mouse_screen + self.camera.position

        entities = self.world.get_nearest_entities(mouse_world, 200)

        clicked_entity = None

        for entity in reversed(entities):
            if entity.bounds.collidepoint(mouse_world):
                clicked_entity = entity
                break

        mods = pygame.key.get_mods()
        shift = mods & pygame.KMOD_SHIFT

        if clicked_entity:

            if shift:
                if clicked_entity not in self.selected_entities:
                    self.selected_entities.append(clicked_entity)
            else:
                self.selected_entities = [clicked_entity]

            self.dragging_entity = clicked_entity
            self.drag_offset = mouse_world - clicked_entity.position
        else:
            if not shift:
                self.selected_entities.clear()
    # Scene methods
    def handle_pygame_event(self, event):
        if not self.window_manager.current_window:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                self._left_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Правая кнопка мыши
                self._right_click(event)
            if event.type == pygame.MOUSEMOTION:
                if self.dragging_entity:

                    mouse_world = pygame.Vector2(event.pos) + self.camera.position
                    new_pos = mouse_world - self.drag_offset

                    move_delta = new_pos - self.dragging_entity.position

                    for entity in self.selected_entities:
                        entity.position += move_delta

                    if self.use_grid:
                        grid_size = 50

                        for entity in self.selected_entities:
                            entity.position.x = int(entity.position.x // grid_size) * grid_size
                            entity.position.y = int(entity.position.y // grid_size) * grid_size
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.dragging_entity = None
            # keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    for entity in self.selected_entities:
                        entity.rotation += 90
                        if entity.rotation == 360:
                            entity.rotation = 0
        self.ui.handle_pygame_event(event)
        self.window_manager.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        if not self.window_manager.current_window:
            # World
            self.world.update_all_hitboxes()

        # ui
        self.ui.update(delta, **kwargs)
        self.window_manager.update_current_window(delta)

        # camera movement
        if not self.window_manager.current_window:
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
        self.window_manager.draw_current_window(screen)
