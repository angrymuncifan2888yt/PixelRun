from enum import Enum, auto


class WindowType(Enum):
    LEVEL_EDIT = auto()
    EDIT_SPECIAL_ENTITY = auto()
    EDIT_ENTITY = auto()
    EDIT_ID_ENTITY = auto()