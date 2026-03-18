from window import WindowType
from util import save_file_dialog, open_file_dialog
import json
from level import Serializator, Deserializator
from scene import SceneType
import pygame

def button_edit_special_callback(self):
    self.edit_special_window.entities = self.selected_entities
    self.edit_special_window.load_entity_data()
    self.window_manager.set_window(WindowType.EDIT_SPECIAL_ENTITY)
def button_edit_entity_callback(self):
    self.entity_edit_window.entities = self.selected_entities
    self.entity_edit_window.load_entity_data()
    self.window_manager.set_window(WindowType.EDIT_ENTITY)

def button_id_callback(self):
    self.entity_id_edit_window.entities = self.selected_entities
    self.entity_id_edit_window.load_entity_data()
    self.window_manager.set_window(WindowType.EDIT_ID_ENTITY)
def button_save_callback(self):
    if not self.level_path:
        level_path = save_file_dialog(
            "Save level",
            [("JSON Files", "*.json")],
            ".json"
        )
        if level_path:
            if not level_path.endswith(".json"):
                level_path += ".json"
            with open(level_path, "w") as f:
                self._form_level()
                json.dump(Serializator.get_level_json(self.level), f, indent=4)
            self.level_path = level_path
    else:
        with open(self.level_path, "w+") as f:
            self._form_level()
            json.dump(Serializator.get_level_json(self.level), f, indent=4)

def button_load_callback(self):
    level_path = open_file_dialog(
        "Load level",
        [("JSON Files", "*.json")]
    )

    if not level_path:
        return

    with open(level_path, "r") as f:
        level_json = json.load(f)

    self.level = Deserializator.load_level(level_json)
    self.world.entities.clear()
    for obj in self.level.objects:
        entity = Deserializator.load_entity(obj, self.world)
        self.world.add_entity(entity)

    self.level_path = level_path

def button_play_callback(self):
    self._form_level()
    game_scene = self.scene_manager.get_scene(SceneType.EDITOR_PLAYTEST)
    game_scene.load_level(self.level)
    self.scene_manager.set_scene(SceneType.EDITOR_PLAYTEST)

def button_edit_level_callback(self):
    self.window_manager.set_window(WindowType.LEVEL_EDIT)
    self.level_edit_window.update_data(*self.level.background_color, self.level.name, self.level.player_spawn)
def button_hitbox_callback(self):
    self.show_hitboxes = not self.show_hitboxes
    if self.show_hitboxes:
        self.btn_hitbox.color = (0, 200, 0)
        self.btn_hitbox.hover_color = (0, 150, 0)
    else:
        self.btn_hitbox.color = (200, 0, 0)
        self.btn_hitbox.hover_color = (150, 0, 0)
        
def button_grid_callback(self):
    self.use_grid = not self.use_grid

    if self.use_grid:
        self.btn_grid.color = (0, 200, 0)
        self.btn_grid.hover_color = (0, 150, 0)
    else:
        self.btn_grid.color = (200, 0, 0)
        self.btn_grid.hover_color = (150, 0, 0)
def button_delete_callback(self):
    for entity in self.selected_entities:
        self.world.remove_entity(entity)

    self.selected_entities.clear()
def button_copy_callback(self):
    if not self.selected_entities:
        return

    self.entity_buffer = []

    base_pos = self.selected_entities[0].position

    for entity in self.selected_entities:
        data = Serializator.get_entity_json(entity)

        offset = entity.position - base_pos

        data["_offset"] = (offset.x, offset.y)

        self.entity_buffer.append(data)
def button_paste_callback(self):
    if not self.entity_buffer:
        return

    center_world = pygame.Vector2(
        self.camera.position.x + self.camera.width / 2,
        self.camera.position.y + self.camera.height / 2
    )

    new_entities = []

    for data in self.entity_buffer:

        offset = pygame.Vector2(data["_offset"])

        entity = Deserializator.load_entity(data, self.world)

        entity.position = center_world + offset

        if self.use_grid:
            grid = 50
            entity.position.x = int(entity.position.x // grid) * grid
            entity.position.y = int(entity.position.y // grid) * grid

        self.world.add_entity(entity)

        new_entities.append(entity)

    self.selected_entities = new_entities
