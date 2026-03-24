from scene import Scene
from util import Camera
from core import World, Platform, Spike, Trigger
from core.render import render_entity, render_hitbox
from data import const
from level import Level
from .edit_level_window import LevelEditWindow
from .edit_entity_window import EditEntityWindow
from window import WindowManager
from .scene_editor_buttons import *
from .edit_entity_id_window import EditEntityIDWindow
from.edit_special_window import EditSpecialWindow
from .scene_editor_ui import create_ui
import pygame


class SceneEditor(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager, SceneType.EDITOR)

        create_ui(self)

        self.level = Level()
        self.level_path = None
        self.world = World()
        self.show_hitboxes = False
        self.camera = Camera(pygame.Vector2(0, 0), *const.WINDOW_SIZE)
        self.selected_entities = []
        self.entity_buffer = None
        self.use_grid = True
        self.dragging_entity = None
        self.drag_offset = pygame.Vector2(0, 0)

        self.selection_start = None
        self.selection_rect = None
        self.is_selecting = False

        self.world.add_entity(Platform(self.world, pygame.Vector2(0, 0)))
        self.world.add_entity(Spike(self.world, pygame.Vector2(300, 300)))

        self.window_manager = WindowManager()
        self.level_edit_window = LevelEditWindow(
            self.window_manager,
            const.WINDOW_SIZE,
            set_bg_func=self._set_level_background,
            set_spawn_func=self._set_player_spawn,
            set_name_func=self._set_level_name,
            delete_level_objects_func=self._delete_all_objects
        )
        self.entity_edit_window = EditEntityWindow(self.window_manager, self.selected_entities, const.WINDOW_SIZE)
        self.entity_id_edit_window = EditEntityIDWindow(self.window_manager, self.selected_entities, const.WINDOW_SIZE)
        self.edit_special_window = EditSpecialWindow(self.window_manager, self.selected_entities, const.WINDOW_SIZE)
        self.window_manager.add_window(self.level_edit_window)
        self.window_manager.add_window(self.entity_id_edit_window)
        self.window_manager.add_window(self.entity_edit_window)
        self.window_manager.add_window(self.edit_special_window)

    def _back_to_menu(self):
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

    def _set_level_background(self, r, g, b):
        self.level.background_color = (r, g, b)

    def _set_player_spawn(self, x, y):
        self.level.player_spawn = pygame.Vector2(x, y)

    def _set_level_name(self, name):
        self.level.name = name

    def _delete_all_objects(self):
        self.world.entities.clear()
        self.level.objects.clear()

    def _draw_world(self, screen):
        grid_size = 50
        grid_color = (60, 60, 60)
        start_x = int(self.camera.position.x // grid_size * grid_size)
        end_x = int(self.camera.position.x + self.camera.width)
        start_y = int(self.camera.position.y // grid_size * grid_size)
        end_y = int(self.camera.position.y + self.camera.height)

        for x in range(start_x, end_x, grid_size):
            pygame.draw.line(screen, grid_color, (x - self.camera.position.x, 0),
                             (x - self.camera.position.x, self.camera.height))
        for y in range(start_y, end_y, grid_size):
            pygame.draw.line(screen, grid_color, (0, y - self.camera.position.y),
                             (self.camera.width, y - self.camera.position.y))

        entities = self.world.get_nearest_entities(self.camera.position, 2000)
        for entity in entities:
            if self.camera.is_object_visible(entity.position, entity.width, entity.height):
                if isinstance(entity, Trigger):
                    old_opacity = entity.opacity
                    entity.opacity = 255
                    render_entity(screen, entity, self.camera)
                    entity.opacity = old_opacity
                else:
                    render_entity(screen, entity, self.camera)
                if self.show_hitboxes:
                    render_hitbox(screen, entity.hitbox, self.camera)
                if entity in self.selected_entities:
                    rect = pygame.Rect(
                        entity.position.x - self.camera.position.x,
                        entity.position.y - self.camera.position.y,
                        entity.width, entity.height
                    )
                    pygame.draw.rect(screen, (0, 255, 0), rect, 3)

        if self.selection_rect:
            pygame.draw.rect(screen, (0, 255, 0), self.selection_rect, 2)

    def _form_level(self):
        self.level.objects = [Serializator.get_entity_json(e) for e in self.world.entities]

    def _left_click(self, event):
        mouse_screen = pygame.Vector2(event.pos)
        if self.ui.is_mouse_over_ui(mouse_screen):
            return

        mouse_world = mouse_screen + self.camera.position
        selected_cls = self.entity_panel.get_selected()
        mods = pygame.key.get_mods()
        shift = mods & pygame.KMOD_SHIFT

        # Перемещение выбранных объектов Shift + ЛКМ
        if shift and self.selected_entities:
            clicked_entity = None
            entities = self.world.get_nearest_entities(mouse_world, 200)
            for entity in reversed(entities):
                if entity.bounds.collidepoint(mouse_world):
                    clicked_entity = entity
                    break
            if clicked_entity and clicked_entity in self.selected_entities:
                self.dragging_entity = clicked_entity
                self.drag_offset = mouse_world - clicked_entity.position

        # Создание нового объекта
        elif selected_cls:
            if self.use_grid:
                grid_size = 50
                mouse_world.x = int(mouse_world.x // grid_size) * grid_size
                mouse_world.y = int(mouse_world.y // grid_size) * grid_size
            entity = selected_cls(self.world, mouse_world)
            self.world.add_entity(entity)

        # Выделение объекта обычной ЛКМ
        else:
            clicked_entity = None
            entities = self.world.get_nearest_entities(mouse_world, 200)
            for entity in reversed(entities):
                if entity.bounds.collidepoint(mouse_world):
                    clicked_entity = entity
                    break
            shift = mods & pygame.KMOD_SHIFT
            if clicked_entity:
                if shift and clicked_entity not in self.selected_entities:
                    self.selected_entities.append(clicked_entity)
                else:
                    self.selected_entities = [clicked_entity]
            else:
                if not shift:
                    self.selected_entities.clear()

    def _right_click(self, event):
        mouse_screen = pygame.Vector2(event.pos)
        if self.ui.is_mouse_over_ui(mouse_screen):
            return

        mouse_world = mouse_screen + self.camera.position
        clicked_entity = None
        entities = self.world.get_nearest_entities(mouse_world, 200)
        for entity in reversed(entities):
            if entity.bounds.collidepoint(mouse_world):
                clicked_entity = entity
                break

        mods = pygame.key.get_mods()
        shift = mods & pygame.KMOD_SHIFT

        # ПКМ по объекту → выделяем
        if clicked_entity:
            if shift and clicked_entity not in self.selected_entities:
                self.selected_entities.append(clicked_entity)
            else:
                self.selected_entities = [clicked_entity]
        # ПКМ по пустому месту → начинаем рамку
        else:
            self.is_selecting = True
            self.selection_start = mouse_screen
            self.selection_rect = pygame.Rect(mouse_screen.x, mouse_screen.y, 0, 0)

    def handle_pygame_event(self, event):
        if not self.window_manager.current_window:
            mouse_screen = pygame.Vector2(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._left_click(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_entity = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self._right_click(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if self.is_selecting:
                    self.selected_entities.clear()
                    if self.selection_rect:
                        rect_world = self.selection_rect.move(self.camera.position)
                        for entity in self.world.entities:
                            ent_rect = pygame.Rect(entity.position.x, entity.position.y, entity.width, entity.height)
                            if rect_world.colliderect(ent_rect):
                                self.selected_entities.append(entity)
                    self.is_selecting = False
                    self.selection_rect = None

            if event.type == pygame.MOUSEMOTION:
                if self.is_selecting:
                    x = min(self.selection_start.x, mouse_screen.x)
                    y = min(self.selection_start.y, mouse_screen.y)
                    w = abs(mouse_screen.x - self.selection_start.x)
                    h = abs(mouse_screen.y - self.selection_start.y)
                    self.selection_rect = pygame.Rect(x, y, w, h)

                if self.dragging_entity:
                    mouse_world = mouse_screen + self.camera.position
                    new_pos = mouse_world - self.drag_offset
                    move_delta = new_pos - self.dragging_entity.position
                    for entity in self.selected_entities:
                        entity.position += move_delta
                    if self.use_grid:
                        grid_size = 50
                        for entity in self.selected_entities:
                            entity.position.x = int(entity.position.x // grid_size) * grid_size
                            entity.position.y = int(entity.position.y // grid_size) * grid_size

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                for entity in self.selected_entities:
                    entity.rotation += 90
                    if entity.rotation == 360:
                        entity.rotation = 0

        if not self.window_manager.current_window:
            self.ui.handle_pygame_event(event)
        self.window_manager.handle_pygame_event(event)

    def update(self, delta, **kwargs):
        if not self.window_manager.current_window:
            self.world.update_all_hitboxes()
        self.ui.update(delta, **kwargs)
        self.window_manager.update_current_window(delta)

        if not self.window_manager.current_window:
            keys = pygame.key.get_pressed()
            speed = 2000
            if keys[pygame.K_w]:
                self.camera.position.y -= speed * delta
            if keys[pygame.K_s]:
                self.camera.position.y += speed * delta
            if keys[pygame.K_a]:
                self.camera.position.x -= speed * delta
            if keys[pygame.K_d]:
                self.camera.position.x += speed * delta

    def draw(self, screen):
        screen.fill(self.level.background_color)
        self._draw_world(screen)
        self.ui.draw(screen)
        self.window_manager.draw_current_window(screen)
