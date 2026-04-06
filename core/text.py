from .entity import Entity
from data.fonts import Fonts
import pygame


class Text(Entity):
    def __init__(self, world, position: pygame.Vector2, width=100, height=100, rotation=0, text="Text", color=(255, 255, 255)):
        super().__init__(world, position, width, height, rotation)
        self.color = color
        self.text = text
        self.auto_resize = True

        self._text_surface = None
        self._dirty = True
    def _update_surface(self):
        self._text_surface = Fonts.NORMAL_30.render(self.text, True, self.color)

        if self.auto_resize:
            self.width = self._text_surface.get_width()
            self.height = self._text_surface.get_height()

        self._dirty = False
    def get_special_fields(self):
        return {
            "r": {"type": "int", "value": self.color[0]},
            "g": {"type": "int", "value": self.color[1]},
            "b": {"type": "int", "value": self.color[2]},
            "text": {"type": "str", "value": self.text},
            "auto_resize": {"type": "bool", "value": self.auto_resize}
        }


    def apply_special_fields(self, data):
        try:
            self.color = (
                int(data.get("r", self.color[0])),
                int(data.get("g", self.color[1])),
                int(data.get("b", self.color[2])),
            )
            self.text = str(data.get("text", self.text))
            self.auto_resize = bool(data.get("auto_resize", self.auto_resize))

            self._dirty = True

        except:
            pass
