from typing import Any


class Scene:
    def __init__(self, scene_manager, id_: Any) -> None:
        self.id = id_
        self.scene_manager = scene_manager

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_pygame_event(self, event):
        pass

    def update(self, delta, **kwargs):
        pass

    def draw(self, screen):
        pass