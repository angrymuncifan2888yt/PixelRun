from enum import Enum, auto


class EventType(Enum):
    TEST_EVENT = auto()
    PLAYER_JUMP = auto()
    PLAYER_TOUCH_END_DOOR = auto()
