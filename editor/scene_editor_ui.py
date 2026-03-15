import pygame
from data import Fonts
from scene import SceneType
from ui import NormalButton, UiManager
from data import const
from .scene_editor_buttons import *
from .entity_panel import EntityPanel

def create_ui(self) -> None:
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
        callback=lambda: button_copy_callback(self)
    )
    # Кнопка Paste
    btn_paste = NormalButton(
        position=pygame.Vector2(const.WINDOW_SIZE[0] - 220, 10),
        size=(100, 100),
        text="Paste",
        font=Fonts.NORMAL_30,
        callback=lambda: button_paste_callback(self)
    )
    # Кнопка Edit
    btn_edit = NormalButton(
        position=pygame.Vector2(const.WINDOW_SIZE[0] - 220, 120),
        size=(100, 100),
        text="Edit",
        font=Fonts.NORMAL_30,
        callback=lambda: button_edit_entity_callback(self)
    )        
    # Кнопка Edit id
    btn_edit_id = NormalButton(
        position=pygame.Vector2(const.WINDOW_SIZE[0] - 330, 10),
        size=(100, 100),
        text="ID",
        font=Fonts.NORMAL_30,
        callback=lambda: button_id_callback(self)
    )        
    # Кнопка Delete
    btn_delete = NormalButton(
        position=pygame.Vector2(const.WINDOW_SIZE[0] - 110, 120),
        size=(100, 100),
        text="Delete",
        font=Fonts.NORMAL_30,
        callback=lambda: button_delete_callback(self)
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
        callback=lambda: button_edit_level_callback(self)
    )        
    btn_edit_level.center_by_x(const.WINDOW_SIZE[0])

    # Кнопка Play
    btn_play = NormalButton(
        position=pygame.Vector2(10, const.WINDOW_SIZE[1] - 330),
        size=(100, 100),
        text="Play",
        font=Fonts.NORMAL_30,
        callback=lambda: button_play_callback(self)
    )    
    # Кнопка Save
    btn_save = NormalButton(
        position=pygame.Vector2(10, const.WINDOW_SIZE[1] - 220),
        size=(100, 100),
        text="Save",
        font=Fonts.NORMAL_30,
        callback=lambda: button_save_callback(self)
    )
    # Кнопка Load
    btn_load = NormalButton(
        position=pygame.Vector2(10, const.WINDOW_SIZE[1] - 110),
        size=(100, 100),
        text="Load",
        font=Fonts.NORMAL_30,
        callback=lambda: button_load_callback(self)
    )
    # Кнопка Hitbox
    self.btn_hitbox = NormalButton(
        position=pygame.Vector2(const.WINDOW_SIZE[0] - 110, const.WINDOW_SIZE[1] - 110),
        size=(100, 100),
        text="Hitbox",
        font=Fonts.NORMAL_30,
        color=(200, 0, 0),
        callback=lambda: button_hitbox_callback(self)
    )
    self.btn_hitbox.hover_color = (150, 0, 0)
    # Кнопка Grid
    self.btn_grid = NormalButton(
        position=pygame.Vector2(const.WINDOW_SIZE[0] - 110, const.WINDOW_SIZE[1] - 220),
        size=(100, 100),
        text="Grid",
        font=Fonts.NORMAL_30,
        color=(0, 200, 0),
        callback=lambda: button_grid_callback(self)
    )
    self.btn_grid.hover_color = (0, 150, 0)

    self.entity_panel = EntityPanel(
        position=pygame.Vector2(10, 70),
        width=240,
        height=390
    )

    self.ui.add_ui_object(self.btn_hitbox)
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
    self.ui.add_ui_object(self.btn_grid)
    self.ui.add_ui_object(self.entity_panel)
    self.ui.add_ui_object(btn_edit_id)