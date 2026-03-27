import pygame
from ui import NormalButton, LineEdit
from ui.ui_manager import UiManager
from data import Fonts
from window import Window, WindowType


class EditSpecialWindow(Window):

    def __init__(self, manager, entities, screen_size):
        super().__init__(manager, WindowType.EDIT_SPECIAL_ENTITY)
